from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class Countdown(TypedDict):
    current: int


def decrease_one(state: Countdown):
    new_current = state["current"] - 1
    print("i reduced it by 1")
    return {
        "current": new_current
    }


def router(state: Countdown):
    if state["current"] > 0:
        return "go_again"
    else:
        return "done"


workflow = StateGraph(Countdown)
workflow.add_node("dec_one", decrease_one)

workflow.add_edge(START, "dec_one")

workflow.add_conditional_edges(
    "dec_one",
    router,
    {
        "done": END,
        "go_again": "dec_one"
    }
)

app = workflow.compile()
output = app.invoke({"current": 5})
print(output)
