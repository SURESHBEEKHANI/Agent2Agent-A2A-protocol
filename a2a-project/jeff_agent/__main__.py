# ============================================
# Step 3: Agent Card Definition & Hosting
# ============================================

# Import core A2A metadata types
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)


# Import agent logic
from agent import JeffAgent

# Import A2A server components
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import JeffAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication

# ASGI server for running the application
import uvicorn


# ============================================
# Main Application Entry Point
# ============================================

def main(host="localhost", port=10004):
    """
    Bootstraps and runs the A2A agent server.

    This function:
    1. Defines the agent skill (what the agent can do)
    2. Creates the Agent Card (agent metadata)
    3. Configures the request handler
    4. Starts the Starlette-based A2A server
    """

    # --------------------------------------------
    # Define Agent Skill
    # --------------------------------------------

    # AgentSkill describes a specific capability of the agent.
    # Skills help discovery, orchestration, and tool routing
    # in multi-agent ecosystems.
    skill = AgentSkill(
        id="schedule_badminton",
        name="Badminton Scheduling Tool",
        description="Helps with finding Jeff's availability for Badminton",
        tags=["scheduling", "badminton"],
        examples=["Are you free to play badminton on 2025-11-05?"]
    )

    # --------------------------------------------
    # Create Agent Card (Agent Metadata)
    # --------------------------------------------

    # AgentCard acts as the public identity of the agent.
    # It defines:
    # - Name & description
    # - URL endpoint
    # - Supported input/output types
    # - Skills & capabilities
    agent_card = AgentCard(
        name="Jeff's Agent",
        description="Helps with scheduling badminton games",
        url=f"http://{host}:{port}/",
        version="1.0.0",

        # Input/output content types supported by the agent
        defaultInputModes=JeffAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=JeffAgent.SUPPORTED_CONTENT_TYPES,

        # Capabilities can include streaming, push notifications, etc.
        capabilities=AgentCapabilities(),

        # List of skills exposed by this agent
        skills=[skill]
    )

    # ============================================
    # Step 4: Host the Agent (Server Layer)
    # ============================================
    #httpx_clien =httpx.Asyncclent()
    # Create request handler
    # This connects:
    # - Incoming HTTP requests
    # - Agent Executor (business logic)
    # - Task storage system
    request_handler = DefaultRequestHandler(
        agent_executor=JeffAgentExecutor(),

        # In-memory task store (good for development/testing)
        # In production, replace with persistent store (Redis, DB, etc.)
        task_store=InMemoryTaskStore(),

        # Optional: Push notifier for async callbacks
        # push_notifier=InMemoryPushNotifier(httpx_client),
    )

    # --------------------------------------------
    # Create Starlette-based A2A Application
    # --------------------------------------------

    # A2AStarletteApplication wraps:
    # - AgentCard metadata
    # - Request handler
    # - HTTP routing layer
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    # --------------------------------------------
    # Run the ASGI Server
    # --------------------------------------------

    # Launch the application using Uvicorn
    # Accessible at: http://localhost:10004/
    uvicorn.run(
        server.build(),
        host=host,
        port=port
    )


# ============================================
# Script Execution Guard
# ============================================

# Ensures the server runs only when file is executed directly
if __name__ == "__main__":
    main()
