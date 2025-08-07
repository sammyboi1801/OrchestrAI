from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Literal, Optional
from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.supervisor_agent import supervisor_node
from agents.orchestrator_agent import orchestrator_node
from agents.researcher_agent import research_node
from agents.coder_agent import code_node
from agents.general_agent import general_node
from agents.researcher_agent import research_node
from agents.RAG_agent import RAG_node
import pprint

from tools.map_tools import FIND_NEARBY_PLACES
graph = StateGraph(MessagesState)

graph.add_node("supervisor", supervisor_node)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("researcher", research_node)
graph.add_node("coder", code_node)
graph.add_node("general", general_node)
graph.add_node("rag", RAG_node)

graph.add_edge(START, "orchestrator")
app = graph.compile()

mermaid_code = app.get_graph().draw_mermaid()
# print(mermaid_code)

inputs = {
    "messages": [
        ("user", "What does the research paper that I have uploaded about?"),
    ]
}

for event in app.stream(inputs):
    for key, value in event.items():
        if value is None:
            continue
        last_message = value.get("messages", [])[-1] if "messages" in value else None
        if last_message:
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint(last_message, indent=2, width=80, depth=None)
            print()