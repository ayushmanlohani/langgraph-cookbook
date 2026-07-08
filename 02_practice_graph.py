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
        "log": state["log"] + [" Order Received"]
    }


def second_node(state: OrderProcessing):
    print("-> Confirming order")
    return {}

# Okay so these are only steps in the workflow or as you say "NODES"
# Now we gotta make the actual GRAPH


workflow = StateGraph(OrderProcessing)

# so we basically start the making process with command and now we have to add the nodes her
# and these nodes are just present till now, they are not even conncted

workflow.add_node("node_A", first_node)
workflow.add_node("node_B", second_node)

# now we will attach them with edges
workflow.add_edge(START, "node_A")
workflow.add_edge("node_A", "node_B")
workflow.add_edge("node_B", END)

# then we compile this badboy
app = workflow.compile()

# Now from here we give it starting data and basically this is our starting point

starting_data = {
    "order_id": "ORD-67",
    "log": []
}
output = app.invoke(starting_data)

print(output)
