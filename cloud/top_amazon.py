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
    product = input("Enter a product to search on Amazon: ")
    if not product.strip():
        print("Product name cannot be empty.")
        return

    client = AsyncBrowserUse(api_key=os.environ["BROWSER_USE_API_KEY"])

    task_prompt = (
        f"Search Amazon for the top 5 most popular products matching '{product}'. "
        "For each product, show its product rating and current price. "
        "Format the output nicely as a markdown list."
    )
    
    task = await client.tasks.create_task(
        task=task_prompt,
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
        output_str = result.output
        if not isinstance(output_str, str):
            import json
            output_str = f"```json\n{json.dumps(output_str, indent=2)}\n```"
        console.print(Markdown(output_str))


if __name__ == "__main__":
    asyncio.run(main())
