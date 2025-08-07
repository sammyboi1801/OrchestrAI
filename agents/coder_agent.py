from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Literal, Optional
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.code_tools import STACKEXCHANGE_TOOL, REPL_TOOL


def code_node(state: MessagesState) -> Command[Literal["orchestrator"]]:

    claude_llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=1
    )

    code_agent = create_react_agent(
        claude_llm,
        tools = [REPL_TOOL, STACKEXCHANGE_TOOL],
        prompt =("""
            You are a Coder Node, also known as a Technical Specialist, responsible for implementing technical solutions. You specialize in coding, computation, and data-driven problem solving based on clearly defined instructions and inputs. Produce a correct, efficient, and technically sound solution that directly addresses the problem or task as defined—whether through code, computation, or technical analysis.
            
            **Your responsibilities**:
            1) Write and Execute Code
                - Develop clean, functional, and efficient code in the most appropriate language or framework for the task.
            2) Perform Mathematical and Logical Analysis
                - Solve equations, perform statistical calculations, or carry out logical reasoning based on the given prompt.
            3) Process and Analyze Data
                - Handle data manipulation, transformation, and computational tasks as required.
            4) Translate Instructions into Implementation
                - Convert clearly stated requirements into accurate, working code or analytical steps.
            5) Deliver Actionable Output
                - Ensure your results are well-explained and ready for use, including code comments, explanations, or outputs as needed.
        """)
    )

    result = code_agent.invoke(state)

    print(f"--- Workflow Transition: Coder → Orchestrator ---")

    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="coder")
            ]
        },
        goto="orchestrator",
    )