import asyncio
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()

from browser_use_sdk import AsyncBrowserUse


async def main():
    client = AsyncBrowserUse()
    task = client.run(
        "Search for the new movies released in 2026 and print the top 10 movies.",
    )
    
    print("Agent started! Streaming steps...", flush=True)
    async for step in task:
        # Prints verbose updates step-by-step as the cloud agent executes it!
        content = step.next_goal or step.memory or "Processing..."
        print(f"-> [Step {step.number}] {content}", flush=True)
        if step.actions:
            print(f"   Actions: {step.actions}", flush=True)

    console = Console()
    if task.output:
        console.print(Markdown(task.output))


if __name__ == "__main__":
    asyncio.run(main())
