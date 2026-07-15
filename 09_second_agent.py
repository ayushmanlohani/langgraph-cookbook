from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.messages import HumanMessage
from datetime import datetime

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    tool_to_use: str
    result: str


@tool
def calculator(expression: str):
    """Evaluates a basic math expression, e.g. '12 * 4'."""
    return str(eval(expression))


@tool
def counter(sentence: str):
    """Counts words and characters in a sentence."""

    word, characters = 0, len(sentence)
    for i in range(len(sentence)):
        if i == 0:
            if sentence[i] != " ":
                word += 1
        else:
            if sentence[i] != " " and sentence[i-1] == " ":
                word += 1

    return {
        "word": word,
        "characters": characters
    }
