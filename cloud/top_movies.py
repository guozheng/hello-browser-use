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
    task = await client.tasks.create_task(
        task="Search for the new movies released in 2026 and print the top 10 movies. Return the result directly as formatted markdown. Do NOT write your results to any JSON file and do NOT mention saving to output.json in your final answer.",
        llm="gemini-3-flash-preview"
    )
    
    print("Agent started! Streaming steps...", flush=True)
    step_num = 1
    async for step in task.stream():
        print(f"-> [Step {step_num}] {step.next_goal}", flush=True)
        step_num += 1

    result = await task.complete()
    console = Console()
    if result.output:
        console.print(Markdown(result.output))
        
        from datetime import datetime
        from workspace_util import upload_string_to_workspace
        
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M.md")
        
        print("\nUploading output to 'top-movies' workspace...", flush=True)
        workspace_id = await upload_string_to_workspace(
            client=client,
            workspace_name="top-movies",
            content=result.output,
            filename=filename
        )
        print(f"Successfully uploaded! (Workspace ID: {workspace_id})", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
