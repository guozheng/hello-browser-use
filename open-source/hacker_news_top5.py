from browser_use import Agent, ChatBrowserUse, ChatGoogle, BrowserProfile, ChatAnthropic, ChatGroq
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    #llm = ChatBrowserUse()
    llm = ChatGoogle(model='gemini-2.5-flash-lite')
    #llm = ChatAnthropic(model='claude-haiku-4-5-20251001')
    #llm = ChatGroq(model='llama-3.3-70b-versatile')
    task = "Find the top 5 most popular post on Hacker News and print the result."
    # if your Chrome path is different, set that in the browser profile
    profile = BrowserProfile(executable_path='/Volumes/Data/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    agent = Agent(task=task, llm=llm, browser_profile=profile)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())