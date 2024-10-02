import json
from pydantic import BaseModel, Field
from typing import Literal, cast, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage

from copilotkit.langchain import copilotkit_customize_config

class WeatherResponse(BaseModel):
    """Respond to the user with this"""

    temperature: float = Field(description="The temperature in fahrenheit")
    wind_direction: str = Field(
        description="The direction of the wind in abbreviated form"
    )
    wind_speed: float = Field(description="The speed of the wind in km/h")
    # temperature: float
    # wind_direction: str
    # wind_speed: float


# Inherit 'messages' key from MessagesState, which is a list of chat messages
class AgentState(MessagesState):
    # Final structured response from the agent
    final_response: WeatherResponse
    input: str

@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It is cloudy in NYC, with 5 mph winds in the North-East direction and a temperature of 70 degrees"
    elif city == "sf":
        return "It is 75 degrees and sunny in SF, with 3 mph winds in the South-East direction"
    else:
        raise AssertionError("Unknown city")

tools = [get_weather, WeatherResponse]


# Define the function that calls the model
def call_model(state: AgentState, config: RunnableConfig):
    """Chatbot that gets weather forecasts"""

    model_with_response_tool = ChatOpenAI(model="gpt-4o").bind_tools(
        tools, 
        parallel_tool_calls=False,
        tool_choice=(
            None if state["messages"] and
            isinstance(state["messages"][-1], HumanMessage)
            else "WeatherResponse"
        )
    )

    config = copilotkit_customize_config(
        config,
        emit_messages=True,
        emit_intermediate_state=[
            {
                "state_key": "final_response",
                "tool": "get_weather"
            }
        ]
    )

    response = model_with_response_tool.invoke([
        SystemMessage(
            content=f"""
            You are a helpful travel assistant that will gather weather forecast information for a given destination. Don't ask for confirmation, just get the weather forecast.

            The user wants to travel to San Francisco.
            """
        ),
        *state["messages"],
    ], config)

    if hasattr(response, "tool_calls") and len(getattr(response, "tool_calls")) > 0:
        ai_message = cast(AIMessage, response)
        return {
            "messages": [
                response,
                ToolMessage(
                    content="got it!",
                    tool_call_id=ai_message.tool_calls[0]["id"]
                )
            ],
            "final_response": cast(AIMessage, response).tool_calls[0]["args"],
        }

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function that responds to the user
def respond(state: AgentState):
    # Construct the final answer from the arguments of the last tool call
    response = WeatherResponse(**state["messages"][-1].tool_calls[0]["args"])
    # We return the final answer
    return {"final_response": response}


# Define the function that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is only one tool call and it is the response tool call we respond to the user
    if (
        len(last_message.tool_calls) == 1
        and last_message.tool_calls[0]["name"] == "WeatherResponse"
    ):
        return "respond"
    # Otherwise we will use the tool node again
    else:
        return "continue"


workflow = StateGraph(AgentState)

# Our workflow will cycle between these two nodes — tools, which
# fetch data or perform actions, and the agent that interacts with
# our users
workflow.add_node("agent", call_model)
workflow.add_node("respond", respond)
workflow.add_node("tools", ToolNode(tools))

# Having added these nodes to the graph, now let's add some edges.

# First, we set the entrypoint as `agent` — i.e., this workflow
# should always begin with the AI agent as opposed to a tool.
workflow.set_entry_point("agent")


workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "respond": "respond",
    },
)

# And here we add a normal edge from `tools` to `agent`, so that
# agents are invoked after a tools call so they can receive and
# process the data returned by the tool
workflow.add_edge("tools", 'agent')
workflow.add_edge("respond", END)

# That's our workflow.

# Finally, we compile it! Here we're initializing and including
# a memory checkpointer that will persist state across runs
basic_agent_app = workflow.compile(checkpointer=MemorySaver())