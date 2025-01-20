# https://github.com/ScrapeGraphAI/Scrapegraph-ai

from phi.tools.spider import SpiderTools
from phi.tools.firecrawl import FirecrawlTools
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.scrapegraph import ScrapeGraph

# https://scrapegraphai.com/
# https://scrapegraphai.com/

# web_researcher = Agent(
#     name="Web Researcher",
#     model=OpenAIChat(model="gpt-4o"),
#     tools=[ScrapeGraph()],
#     instructions=["Analyze and extract UFO/UAP related information according to the database schema"],
#     show_tool_calls=True,
#     markdown=True,
# )


agent = Agent(tools=[FirecrawlTools(scrape=False, crawl=True)],
              show_tool_calls=True, markdown=True)
agent.print_response("Summarize this https://finance.yahoo.com/")


# Spider

agent = Agent(tools=[SpiderTools()])
agent.print_response(
    'Can you scrape the first search result from a search on "news in USA"?', markdown=True)
