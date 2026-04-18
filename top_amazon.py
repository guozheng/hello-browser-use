import asyncio
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()

from browser_use_sdk.v3 import AsyncBrowserUse


async def main():
    product = input("Enter a product to search on Amazon: ")
    if not product.strip():
        print("Product name cannot be empty.")
        return

    client = AsyncBrowserUse()
    task_prompt = (
        f"Search Amazon for the top 5 most popular products matching '{product}'. "
        "For each product, show its product rating and current price. "
        "Format the output nicely as a markdown list."
    )
    
    task = client.run(task_prompt, model="claude-sonnet-4.6")
    
    print("Agent started! Streaming steps...", flush=True)
    step_num = 1
    async for msg in task:
        if msg.summary:
            print(f"-> [Step {step_num}] {msg.summary}", flush=True)
            step_num += 1

    console = Console()
    if task.output:
        console.print(Markdown(task.output))


if __name__ == "__main__":
    asyncio.run(main())
