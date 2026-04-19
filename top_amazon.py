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

    # Get or create a workspace to use cached scripts
    workspace_name = "default"
    workspace_id = None
    response = await client.workspaces.list()
    for w in response.items:
        if w.name == workspace_name:
            workspace_id = str(w.id)
            break
            
    if not workspace_id:
        workspace = await client.workspaces.create(name=workspace_name)
        workspace_id = str(workspace.id)

    task_prompt = (
        f"Search Amazon for the top 5 most popular products matching '@{{{{{product}}}}}'. "
        "IMPORTANT: When writing the python script, YOU MUST use the parameter dynamically "
        "(from sys.argv) to perform the search; DO NOT hardcode the search URL. "
        "For each product, show its product rating and current price. "
        "Format the output nicely as a JSON array or a markdown list."
    )
    
    task = client.run(task_prompt, model="gemini-3-flash", workspace_id=workspace_id)
    
    print("Agent started! Streaming steps...", flush=True)
    step_num = 1
    async for msg in task:
        if msg.summary:
            print(f"-> [Step {step_num}] {msg.summary}", flush=True)
            step_num += 1

    console = Console()
    if getattr(task, "output", None):
        output_str = task.output
        if not isinstance(output_str, str):
            import json
            output_str = f"```json\n{json.dumps(output_str, indent=2)}\n```"
        console.print(Markdown(output_str))


if __name__ == "__main__":
    asyncio.run(main())
