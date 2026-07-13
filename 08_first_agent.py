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

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# by this hinting (-> dict) we expect func to return a certain datatype that is done to prevent errors and find mistakes later.


llm = ChatGroq(model="openai/gpt-oss-20b")


@tool
def calculator(expression: str) -> str:
    """Evaluates a basic math expression, e.g. '12 * 4'."""
    return str(eval(expression))


llm_with_tools = llm.bind_tools([calculator])


def llm_node(state: AgentState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


tool_node = ToolNode([calculator])

workflow = StateGraph(AgentState)

workflow.add_node("llm_node", llm_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "llm_node")
workflow.add_conditional_edges(
    "llm_node",
    tools_condition,   # prebuilt router
    {
        "tools": "tools",   # if tool call needed, go to tools node
        END: END            # if no tool call, finish
    }
)
workflow.add_edge("tools", "llm_node")

app = workflow.compile()
result = app.invoke({"messages": [HumanMessage("What is 24 * 4?")]})
print(result["messages"][-1].content)
