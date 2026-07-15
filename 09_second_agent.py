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
    messages: Annotated[list, add_messages]


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


@tool
def live_time(time_question: str):
    """Tells live time."""
    current = datetime.now()
    return str(current)


def router(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


llm = ChatGroq(model="openai/gpt-oss-20b")
llm_with_tools = llm.bind_tools([calculator, counter, live_time])


def llm_node(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response]
    }


tool_node = ToolNode([calculator, counter, live_time])

workflow = StateGraph(AgentState)

workflow.add_node("llm_node", llm_node)
workflow.add_node("tool_node", tool_node)

workflow.add_edge(START, "llm_node")
workflow.add_conditional_edges(
    "llm_node",
    router,
    {
        "tools": "tool_node",
        END: END
    }
)
workflow.add_edge("tool_node", "llm_node")

app = workflow.compile()
result = app.invoke({"messages": [HumanMessage(
    "What is 24 * 4?, and what is current time, how many words and cahracters are in this sentence")]})
print(result["messages"][-1].content)
