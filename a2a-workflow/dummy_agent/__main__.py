# Import core A2A types used to define the agent metadata
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

# Uvicorn is an ASGI server used to run FastAPI/Starlette apps
import uvicorn


def main():
    """
    Main function that:
    1. Defines agent skills
    2. Creates the agent card (metadata)
    3. Configures request handling
    4. Starts the A2A server
    """

    # -----------------------------
    # Step 1: Define Agent Skill
    # -----------------------------
    # AgentSkill describes what this agent can do.
    # This is visible to other agents in the A2A ecosystem.
    greeting_skill = AgentSkill(
        id="hello_world",                 # Unique identifier for the skill
        name="Greet",                     # Human-readable name
        description="Return a greeting",  # What this skill does
        tags=["greeting", "hello", "world"],  # Keywords for discoverability
        examples=["Hey", "Hi", "Hello"]   # Example inputs
    )

    # -----------------------------
    # Step 2: Define Agent Metadata (AgentCard)
    # -----------------------------
    # AgentCard is like the "resume" or "identity card" of your agent.
    # It tells other agents what this agent is, what it can do, and how to contact it.
    agent_card = AgentCard(
        name="Greeting Agent",                          # Agent name
        description="A simple agent that returns a greeting",
        url="http://localhost:9999/",                   # Where this agent is hosted
        defaultInputModes=["text"],                     # Accepts text input
        defaultOutputModes=["text"],                    # Returns text output
        skills=[greeting_skill],                        # List of supported skills
        version="1.0.0",                                # Version of agent
        capabilities=AgentCapabilities()                # Advanced capabilities (empty for now)
    )

    # -----------------------------
    # Step 3: Configure Request Handling
    # -----------------------------
    # DefaultRequestHandler handles incoming A2A requests.
    from a2a.server.request_handlers import DefaultRequestHandler

    # Custom agent executor that contains the business logic
    from agent_executor import GreetingAgentExecutor

    # InMemoryTaskStore stores tasks temporarily in RAM
    # (Good for development, not production)
    from a2a.server.tasks import InMemoryTaskStore

    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),  # Executes agent logic
        task_store=InMemoryTaskStore()           # Stores tasks in memory
    )

    # -----------------------------
    # Step 4: Create A2A Server Application
    # -----------------------------
    from a2a.server.apps import A2AStarletteApplication
    
    # A2AStarletteApplication wraps everything into a Starlette app
    server = A2AStarletteApplication(
        http_handler=request_handler,  # Handles incoming HTTP requests
        agent_card=agent_card,         # Exposes agent metadata
    )

    # -----------------------------
    # Step 5: Run Server with Uvicorn
    # -----------------------------
    # Host 0.0.0.0 allows external access
    # Port 9999 is where the agent will run
    uvicorn.run(server.build(), host="0.0.0.0", port=9999)


# Entry point of the script
if __name__ == "__main__":
    main()
