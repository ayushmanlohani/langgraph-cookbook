from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# this file is to practice making the conditional graph.


class OrderProcessing(TypedDict):
    order_id: str
    log: list[str]
    status: str


def first_node(state: OrderProcessing):
    print("We are in the fist node")
    return {
        "log": state["log"] + [" Order Received"]
    }


def second_node(state: OrderProcessing):
    print("-> Confirming order")
    return {}
# okay so the most importnat thing here is "ROUTER FUNCTION"
# its main purpose is to decide the next node


def router(state: OrderProcessing) -> str:
    if state['order_id'].startswith("ORD"):
        return "node_b"
    else:
        return "node_reject"

# okay so maybe router is just deciding, this new node gonna actually reject that


def reject_node(state: OrderProcessing) -> dict:
    print("your order got rejected bruh~")
    return {
        "status": "rejected",
        "log": state["log"] + ["order rejected"]
    }


workflow = StateGraph(OrderProcessing)

workflow.add_node("node_a", first_node)
workflow.add_node("node_b", second_node)
workflow.add_node("reject_node", reject_node)
