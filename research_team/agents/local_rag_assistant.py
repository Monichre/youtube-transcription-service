from phi.tools.file import FileTools
from phi.agent import Agent
from resources import vector_db  # type: ignore
from phi.vectordb.pgvector import PgVector2
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.assistant import Assistant
from typing import Optional, List
from rich.prompt import Prompt
import typer
from pathlib import Path
from research_prompt import research_prompt
from phi.knowledge import PDFKnowledgeBase, CSVKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.storage.assistant.postgres import PgAssistantStorage

# from phi.agent import Agent
# from phi.tools.file import FileTools
local_pdf_kb = PDFKnowledgeBase(
    path=Path(
        "data_layer/knowledge"),
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=db_url,
    )
)

csv_kb = CSVKnowledgeBase(
    path=Path("data/csvs"),
    vector_db=PgVector(
        table_name="csv_documents",
        db_url=db_url,
    )
)

local_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/pdfs",
    # Table name: ai.pdf_documents
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    reader=PDFReader(chunk=True),
)

knowledge_base = CombinedKnowledgeBase(
    sources=[
        url_pdf_knowledge_base,
        website_knowledge_base,
        local_pdf_knowledge_base,
    ],
    vector_db=PgVector(
        # Table name: ai.combined_documents
        table_name="combined_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
)

# Local Files
# agent = Agent(tools=[FileTools()], show_tool_calls=True)
# agent.print_response(
#     "What is the most advanced LLM currently? Save the answer to a file.", markdown=True)


# PDF Analysis Agent
pdf_analyst = Assistant(
    name="PDF Analyst",
    knowledge_base=local_pdf_kb,
    storage=storage,
    model=OpenAIChat(model="gpt-4"),
    instructions=[
        research_prompt
    ],
    use_tools=True,
    show_tool_calls=True,
)


# Comment out after first run
knowledge_base.load(recreate=False)

storage = PgAssistantStorage(
    table_name="pdf_assistant", db_url=vector_db.get_db_connection_local())


def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        # tool_calls=True adds functions to
        # search the knowledge base and chat history
        use_tools=True,
        show_tool_calls=True,
        # Uncomment the following line to use traditional RAG
        # add_references_to_prompt=True,
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    while True:
        try:
            message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
            if message in ("exit", "bye"):
                break
            assistant.print_response(message, markdown=True)
        except Exception as e:
            print(f"[red]Error: {e}[/red]")  # Added error handling
