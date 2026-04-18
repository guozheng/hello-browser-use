import asyncio
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()

from browser_use_sdk import AsyncBrowserUse


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
    
    task = client.run(task_prompt)
    
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
