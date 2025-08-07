from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Literal, Optional
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tools import TAVILY_SEARCH, BRAVE_SEARCH, DUCK_DUCK_GO_SEARCH
from tools.research_tools import ARXIV_SEARCH,  PUBMED_SEARCH

def research_node(state: MessagesState) -> Command[Literal["orchestrator"]]:

    """
        Research agent node that gathers information using web search.
        Takes the current task state, performs relevant research, and returns findings for validation.
    """

    claude_llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=1
    )

    research_agent = create_react_agent(
        claude_llm,
        tools = [TAVILY_SEARCH, BRAVE_SEARCH, DUCK_DUCK_GO_SEARCH],
        prompt = """
                You are a Researcher Node, also referred to as an Information Specialist, with deep expertise in conducting thorough, accurate, and structured research. Your role is to supply the factual foundation needed for downstream processing. Deliver a structured, comprehensive, and source-backed information package that fully satisfies the query's research needs and sets up the next agent (e.g., Coder) for effective execution.
                
                **Your responsibilities**:
                1) Determine Information Requirements
                    - Understand the refined query and identify the essential information needs based on context.
                2) Gather High-Quality Data
                    - Locate relevant, accurate, and up-to-date information from credible and authoritative sources.
                3) Structure Your Findings
                    - Organize the collected data clearly—use bullet points, sections, or tables for readability and efficient consumption.
                4) Cite Sources Where Applicable
                    - Attribute data to its source (e.g., website, journal, dataset) whenever possible to enhance trust and traceability.
                5) Avoid Interpretation or Implementation
                    - Do not perform analysis, write code, or make decisions—focus solely on unbiased information gathering.
            """
        )

    result = research_agent.invoke(state)

    print(f"--- Workflow Transition: Researcher → ORCHESTRATOR ---")

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content,
                    name="researcher"
                )
            ]
        },
        goto="orchestrator",
    )