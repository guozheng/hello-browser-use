import asyncio
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()

from browser_use_sdk import AsyncBrowserUse


async def main():
    console = Console()
    console.print("Starting browser-use...")
    client = AsyncBrowserUse()
    console.print("Running browser-use...")
    result = await client.run(
        "Search for the new movies released in 2026 and print the top 10 movies.",
    )
    console.print(Markdown(result.output))


if __name__ == "__main__":
    asyncio.run(main())
