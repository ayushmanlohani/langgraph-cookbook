from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


class AgentState(TypedDict):
    question: str
    answer: str

# by this hinting (-> dict) we expect func to return a certain datatype that is done to prevent errors and find mistakes later.


def llm_node(state: AgentState) -> dict:
    llm = ChatGroq(model="openai/gpt-oss-20b")
    response = llm.invoke(state["question"])
    return {
        "answer": response.content
    }


workflow = StateGraph(AgentState)
workflow.add_node("llm_node", llm_node)
workflow.add_edge(START, "llm_node")
workflow.add_edge("llm_node", END)

app = workflow.compile()
output = app.invoke({"question": "What is 12 * 4"})
print(output)
