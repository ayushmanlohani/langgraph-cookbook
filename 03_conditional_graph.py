from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# this file is to practice making the conditional graph.


class OrderProcessing(TypedDict):
    order_id: str
    log: list[str]
    status: str
