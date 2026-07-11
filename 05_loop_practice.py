from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# okay so this is going ot be about looping
# looping is just a conditional edge that rather than updating the state it points to som earlier node.


class GuessState(TypedDict):
    attempt: int
    target: int
    guess: int


def guess_node(state: GuessState):
    new_attempt = state["attempt"] + 1
    print(f"-> attempt {new_attempt}")
    return {
        "attempt": new_attempt,
        "guess": new_attempt * 3
    }


def check_router(state: GuessState):
    if state["guess"] == state["target"]:
        return "done"
    else:
        return "retry"


workflow = StateGraph(GuessState)
workflow.add_node("guess_node", guess_node)

workflow.add_edge(START, "guess_node")

workflow.add_conditional_edges(
    "guess_node",
    check_router,
    {
        "done": END,
        "retry": "guess_node"
    }
)

app = workflow.compile()
output = app.invoke({"attempt": 0, "target": 12, "guess": 0})
print(output)
