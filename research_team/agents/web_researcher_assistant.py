from typing import List, Optional
from pathlib import Path
from phi.agent import Agent
from phi.assistant import Assistant
from phi.knowledge import PDFKnowledgeBase, WebsiteKnowledgeBase, CSVKnowledgeBase, CombinedKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.tools.firecrawl import FirecrawlTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.openai import OpenAIChat
from data_layer.external_resources import urls

# Database connection
db_url = "postgresql://user:pass@localhost:5432/ultraterrestrial"

# Knowledge Bases


website_kb = WebsiteKnowledgeBase(
    urls=urls,  # Add your domain URLs
    max_links=10,
    vector_db=PgVector(
        table_name="website_documents",
        db_url=db_url,
    )
)


web_researcher = Agent(
    name="Web Researcher",
    role="Research and analyze UFO/UAP information from web sources",
    model=OpenAIChat(model="gpt-4"),
    tools=[FirecrawlTools(scrape=True, crawl=True), DuckDuckGo()],
    instructions=[
        "Analyze and extract UFO/UAP related information according to the database schema",
        "Focus on verifiable sources and official documentation",
        "Maintain clear relationship mappings between entities",
        "Document source reliability and confidence levels",
    ],
    show_tool_calls=True,
    markdown=True,
)
