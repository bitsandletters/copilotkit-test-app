from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage

from copilotkit.langchain import copilotkit_customize_config

class WeatherResponse(BaseModel):
    """Respond to the user with this"""

    conditions: str = Field(description="Weather conditions in the location")
    temperature: float = Field(description="The temperature in fahrenheit")
    wind_direction: str = Field(
        description="The direction of the wind in abbreviated form"
    )
    wind_speed: float = Field(description="The speed of the wind in km/h")

class AgentState(MessagesState):
    final_response: WeatherResponse
    input: str

@tool
def get_weather(city: str):
    """Use this to get weather information."""
    if city == "nyc":
        return "It is cloudy in NYC, with 5 mph winds in the North-East direction and a temperature of 70 degrees"
    elif city == "sf":
        return "It is 75 degrees and sunny in SF, with 3 mph winds in the South-East direction"
    else:
        return "The weather is boring in {city}, with calm winds and a temperature of 40 degrees"

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
                "tool": "WeatherResponse"
            }
        ]
    )

    response = model_with_response_tool.invoke([
        SystemMessage(
            content=f"""
            You are a helpful travel assistant that will gather weather forecast information for a given destination. Don't ask for confirmation, just get the weather forecast.
            """
        ),
        *state["messages"],
    ], config)

    return {"messages": [response]}

# Define the function that responds to the user
def respond(state: AgentState):
    # Construct the final answer from the arguments of the last tool call
    response = WeatherResponse(**state["messages"][-1].tool_calls[0]["args"])
    
    # We return the final answer, dumping the model data in a JSON-able format
    return {
        "final_response": response.model_dump(mode='json')
    }


# Define the function that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there is only one tool call in the most recent message,
    # and it is the response tool call, we respond to the user
    if (
        len(last_message.tool_calls) == 1
        and last_message.tool_calls[0]["name"] == "WeatherResponse"
    ):
        return "respond"
    
    # Otherwise we will use the tool node again
    else:
        return "continue"


workflow = StateGraph(AgentState)
workflow.set_entry_point("agent")
workflow.add_node("agent", call_model)
workflow.add_node("respond", respond)
workflow.add_node("tools", ToolNode(tools))

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "respond": "respond",
    },
)

workflow.add_edge("tools", 'agent')
workflow.set_finish_point("respond")
# workflow.add_edge("respond", END)

basic_agent_app = workflow.compile(checkpointer=MemorySaver())