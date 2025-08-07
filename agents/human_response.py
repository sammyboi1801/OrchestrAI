from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Literal, Optional
from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


def human_response(state: MessagesState, response: str) -> str:

    human_review = interrupt()

    messages = [
                   {"role": "system", "content": HumanMessage(content = human_review)},
               ] + state["messages"]
