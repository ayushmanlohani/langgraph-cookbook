from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. DEFINE THE STATE
# This dict is the single source of truth passed between all nodes.
class State(TypedDict):
    message: str
    steps_taken: list[str]


# 2. DEFINE THE NODES
# Nodes are just pure Python functions. They take State and return updated values.
def first_node(state: State) -> dict:
    print("-> Inside First Node")
    return {
        "message": state["message"] + " World", 
        "steps_taken": state["steps_taken"] + ["First Node Done"]
    }

def second_node(state: State) -> dict:
    print("-> Inside Second Node")
    return {
        "steps_taken": state["steps_taken"] + ["Second Node Done"]
    }


# 3. BUILD THE GRAPH
workflow = StateGraph(State)

# Add our nodes to the canvas
workflow.add_node("node_a", first_node)
workflow.add_node("node_b", second_node)

# Connect the nodes with edges
workflow.add_edge(START, "node_a")  # Entry point
workflow.add_edge("node_a", "node_b") # Flow from a to b
workflow.add_edge("node_b", END)      # Exit point


# 4. COMPILE AND RUN
app = workflow.compile()

# Invoke the graph with the initial data state
initial_data = {"message": "Hello", "steps_taken": []}
final_output = app.invoke(initial_data)

print("\n--- Final Execution Output ---")
print(final_output)