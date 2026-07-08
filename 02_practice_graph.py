from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# first we gotta define the state
# today i will make state named orderprocessing


class OrderProcessing(TypedDict):
    order_id: str
    log: list[str]

# so this can be understood like a box, that will move through the whole factory line.
# and people (nodes) will do stuff to it. ;)

# okay, so now we will define the nodes, i.e the work that will be done


def first_node(state: OrderProcessing):
    print("We are in the fist node")
    return {
        "log": state["log"] + " Order Received"
    }
