from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class AuthState(TypedDict):
    attempts: int
    password: str
    correct_password: str
    status: str


def start_node(state: AuthState):
    print(" Starting Auth")
    return {
        "attempts": 0
    }


def try_password_node(state: AuthState):
    if state["password"] == state["correct_password"]:
        ans = "correct"
    else:
        ans = "wrong"

    return {
        "attempts": state["attempts"] + 1,
        "status":  ans
    }


def router(state: AuthState):
    if state["status"] == "correct":
        return "success"
    elif state["attempts"] >= 3:
        return "locked"
    else:
        return "retry"


def sucess_node(state: AuthState):
    return {"status": "success"}


def lockout_node(state: AuthState):
    return {"status": "locked"}


workflow = StateGraph(AuthState)

workflow.add_node("start_node", start_node)
workflow.add_node("try_pass", try_password_node)
workflow.add_node("sucess", sucess_node)
workflow.add_node("locked", lockout_node)

workflow.add_edge(START, "start_node")
workflow.add_edge("start_node", "try_pass")
workflow.add_conditional_edges(
    "try_pass",
    router,
    {
        "success": "sucess",
        "locked": "locked",
        "retry": "try_pass"
    }
)

workflow.add_edge("sucess", END)
workflow.add_edge("locked", END)

app = workflow.compile()

output = app.invoke(
    {"password": "hellothere", "correct_password": "hello"})
print(output)
