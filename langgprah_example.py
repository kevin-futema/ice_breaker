# First we initialize the model we want to use.
from langchain_ollama import ChatOllama

model = ChatOllama(model="mistral", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]

# We can add our system prompt here

prompt = "Respond in Italian"

# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools, state_modifier=prompt)


inputs = {"messages": [("user", "What's the weather in NYC?")]}

print_stream(graph.stream(inputs, stream_mode="values"))
