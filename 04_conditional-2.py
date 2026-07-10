from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# okay new day new conditional pracice
# new scenario - weather agent


class WeatherState(TypedDict):
    city: str
    temp: str
    advice: str


def fetch_temp_node(state: WeatherState):
    print("-> fetching temp")
    return {"temp": 35}


def hot_node(state: WeatherState):
    print("-> Hot path")
    return {"advice": "Wear light clothes"}


def cold_node(state: WeatherState):
    print("-> Cold path")
    return {"advice": "Wear a jacket"}


def temp_router(state: WeatherState):
    if state["temp"] > 25:
        return "hot"
    else:
        return "cold"


workflow = StateGraph(WeatherState)
workflow.add_node("temp check karne wala node", fetch_temp_node)
workflow.add_node("garam wala node", hot_node)
workflow.add_node("thanda node", cold_node)

workflow.add_edge(START, "temp check karne wala node")

workflow.add_conditional_edges(
    "temp check karne wala node",
    temp_router,
    {
        "hot": "hot_node",
        "cold": "cold_node"
    }
)

workflow.add_edge("garam wala node", END)
workflow.add_edge("thanda node", END)

app = workflow.compile()
starting_data = {
    "city": "Lucknow"
}

output = app.invoke(starting_data)
print(output)
