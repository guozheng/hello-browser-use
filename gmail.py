import asyncio
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()

from browser_use_sdk.v3 import AsyncBrowserUse

async def main():
    client = AsyncBrowserUse()
    
    profiles_response = await client.profiles.list(query="bot-profile")
    if profiles_response.items:
        profile = profiles_response.items[0]
    else:
        profile = await client.profiles.create(name="bot-profile")
    
    session = await client.sessions.create(profile_id=profile.id, model="gemini-3-flash")
    print(f"Live view: {session.live_url}")

    login_task = client.run(
        "Log into gmail with the user aibluejay.mountain@gmail.com",
        session_id=session.id,
        model="gemini-3-flash"
    )

    step_num = 1
    async for msg in login_task:
        if msg.summary:
            print(f"-> [Step {step_num}] {msg.summary}", flush=True)
            step_num += 1
    
    check_email_task = client.run(
        "Check the inbox for any emails from 'Google' and print the subject, sender, and timestamp/date of the email.",
        session_id=session.id,
        model="gemini-3-flash"
    )

    async for msg in check_email_task:
        if msg.summary:
            print(f"-> [Step {step_num}] {msg.summary}", flush=True)
            step_num += 1

    console = Console()
    if getattr(check_email_task, "result", None) and getattr(check_email_task.result, "output", None):
        console.print(Markdown(check_email_task.result.output))
    
    await client.sessions.stop(session.id)

if __name__ == "__main__":
    asyncio.run(main())