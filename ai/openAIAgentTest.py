import asyncio
from browser_use import Agent, Browser


async def main():
    browser = Browser(
        use_cloud=False
    )

    agent = Agent(
        task="""
        Open website http://qa.way2automation.com
        then Enter name as JQ
        then Enter phone as 1234567
        then Enter email as jq@mail.com
        """,
        browser=browser,
    )

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
