import asyncio
from rich.console import Console
from rich.markdown import Markdown

import os
import sys

# Add parent directory to sys.path to allow importing from workspace root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from browser_use_sdk import AsyncBrowserUse

async def main():
    client = AsyncBrowserUse(api_key=os.environ["BROWSER_USE_API_KEY"])
    
    # Find or create a profile named "bot-profile"
    profiles_response = await client.profiles.list_profiles()
    profile = None
    for p in profiles_response.items:
        if p.name == "bot-profile":
            profile = p
            break
    if not profile:
        profile = await client.profiles.create_profile(name="bot-profile")
    
    session = await client.sessions.create_session(profile_id=profile.id)
    print(f"Live view: {session.live_url}")

    # Task 1: Log into Gmail
    login_task = await client.tasks.create_task(
        task="Log into gmail with the user aibluejay.mountain@gmail.com",
        session_id=session.id,
        llm="gemini-3-flash-preview"
    )

    step_num = 1
    async for step in login_task.stream():
        print(f"-> [Step {step_num}] {step.next_goal}", flush=True)
        step_num += 1
    
    # Task 2: Check emails
    check_email_task = await client.tasks.create_task(
        task="Check the inbox for unread emails and print the subject, sender, and timestamp/date of the email.",
        session_id=session.id,
        llm="gemini-3-flash-preview"
    )

    async for step in check_email_task.stream():
        print(f"-> [Step {step_num}] {step.next_goal}", flush=True)
        step_num += 1

    # Get final result
    result = await check_email_task.complete()
    console = Console()
    if result.output:
        console.print(Markdown(result.output))
    
    await client.sessions.update_session(session.id, action="stop")

if __name__ == "__main__":
    asyncio.run(main())