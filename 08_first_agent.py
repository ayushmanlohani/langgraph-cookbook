from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


class AgentState(TypedDict):
    question: str
    answer: str

# by this hinting (-> dict) we expect func to return a certain datatype that is done to prevent errors and find mistakes later.


# def llm_node(state: AgentState) -> dict:
llm = ChatGroq(model="openai/gpt-oss-20b")


@tool
def calculator(expression: str) -> str:
    """Evaluates a basic math expression, e.g. '12 * 4'."""
    return str(eval(expression))


llm_with_tools = llm.bind_tools([calculator])

response = llm_with_tools.invoke("waht is 24 * 4?")
print(response.tool_calls)

# return {
#    "answer": response.content
# }
