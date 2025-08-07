import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END, MessagesState
from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Literal, Optional
from langgraph.types import Command
from tools.RAG_tool import RAG_RETRIEVER_TOOL

load_dotenv()


def RAG_node(state: MessagesState) -> Command[Literal["orchestrator"]]:
    # LLM used in the agent
    claude_llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=1
    )

    # Create the RAG Agent
    rag_agent = create_react_agent(
        claude_llm,
        tools=[RAG_RETRIEVER_TOOL],  # You can add more tools here
        prompt=("""
            You are a Retrieval-Augmented Generation (RAG) Node.

            Your role is to retrieve relevant knowledge from a vector store and synthesize it into a coherent and accurate response. 
            If the input query requires specific or detailed knowledge, use the retrieval tool to fetch that information first.

            **Responsibilities**:
            1. Understand the user's query clearly.
            2. Retrieve knowledge using the provided retrieval tool.
            3. Use the knowledge to generate a helpful, grounded, and informative response.
            4. Be precise and technically correct.
        """)
    )

    result = rag_agent.invoke(state)

    print(f"--- Workflow Transition: RAG Node → Orchestrator ---")

    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="rag_node")
            ]
        },
        goto="orchestrator",
    )