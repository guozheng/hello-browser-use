import asyncio
from rich.console import Console
from rich.markdown import Markdown

import os
import sys

# Add parent directory to sys.path to allow importing from workspace root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from browser_use_sdk.v3 import AsyncBrowserUse


async def main():
    client = AsyncBrowserUse()
    task = client.run(
        "Search for the new movies released in 2026 and print the top 10 movies. Return the result directly as formatted markdown. Do NOT write your results to any JSON file and do NOT mention saving to output.json in your final answer.",
        model="gemini-3-flash"
    )
    
    print("Agent started! Streaming steps...", flush=True)
    step_num = 1
    async for msg in task:
        if msg.summary:
            print(f"-> [Step {step_num}] {msg.summary}", flush=True)
            step_num += 1

    console = Console()
    if task.output:
        console.print(Markdown(task.output))
        
        from datetime import datetime
        from workspace_util import upload_string_to_workspace
        
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M.md")
        
        print("\nUploading output to 'top-movies' workspace...", flush=True)
        workspace_id = await upload_string_to_workspace(
            client=client,
            workspace_name="top-movies",
            content=task.output,
            filename=filename
        )
        print(f"Successfully uploaded! (Workspace ID: {workspace_id})", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
