from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
app = FastAPI()

# Import CopilotKit SDK and integrations
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent

# Import your LangGraph agent; in this example, it's the variable
# named `basic_agent_app` in ./agent.py
from .agent import basic_agent_app

# Initialize the agent for CopilotKit; we'll name it "basic_agent"
basic_agent = LangGraphAgent(
    name="basic_agent",
    description="Agent that asks about the weather",
    agent=basic_agent_app,
)

# Next, initialize the SDK, passing in the agent
sdk = CopilotKitSDK(
    agents=[
        basic_agent
    ],
)

# Finally, add the remote actions endpoint to this API
add_fastapi_endpoint(app, sdk, "/copilotkit")