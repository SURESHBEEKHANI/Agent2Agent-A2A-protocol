# ============================================================
# Standard Library Imports
# ============================================================
import asyncio              # Enables asynchronous execution and event loop management
import uuid                 # Generates globally unique identifiers for message tracking
import datetime             # Provides date/time utilities for runtime context
from typing import List, Dict, Optional  # Adds static typing for improved readability and tooling


# ============================================================
# Third-Party Dependencies
# ============================================================
import httpx                # Async HTTP client for external service communication
import nest_asyncio         # Allows nested asyncio event loops (useful in notebooks/dev environments)

from dotenv import load_dotenv   # Loads environment variables from a .env configuration file


# ============================================================
# Google ADK Core Components
# ============================================================
from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm  # Adapter for external LLM providers via LiteLLM


# ============================================================
# A2A (Agent-to-Agent) Communication Layer
# ============================================================
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,              # Defines metadata schema for remote agents
    MessageSendParams,      # Structured payload model for outgoing messages
    SendMessageRequest,     # Standard A2A request wrapper
    SendMessageResponse,    # Standard A2A response wrapper
)


# ============================================================
# Local Tooling Layer
# ============================================================
from .tools import (
    book_badminton_court,       # Business logic: handles badminton court reservations
    list_court_availabilities,  # Business logic: retrieves available court slots
)


# ============================================================
# Environment Initialization
# ============================================================

# Load environment configuration into the runtime context
load_dotenv()

# Enable nested asyncio support (required when running inside environments
# that already manage an active event loop, such as Jupyter notebooks)
nest_asyncio.apply()


# ============================================================
# RemoteAgentConnection
# ============================================================
class RemoteAgentConnection:
    """
    Represents a managed connection between the Host Agent and a remote A2A-compliant agent.

    Architectural Responsibilities:
    - Maintain an HTTP client session
    - Encapsulate A2A protocol interactions
    - Abstract request/response handling from orchestration logic
    """

    def __init__(self, agent_card: AgentCard, agent_url: str):
        """
        Initialize a remote agent connection.

        Args:
            agent_card (AgentCard): Metadata describing the remote agent's capabilities.
            agent_url (str): Base URL of the remote agent service.
        """
        self.agent_card = agent_card
        self.agent_url = agent_url

        # Dedicated asynchronous HTTP client with defined timeout policy
        self.http_client = httpx.AsyncClient(timeout=30)

        # A2A client responsible for structured inter-agent communication
        self.client = A2AClient(self.http_client, agent_card, url=agent_url)

    async def send_message( self,message_request: SendMessageRequest) -> SendMessageResponse:
        """
        Dispatch a structured message to the remote agent.

        Args:
            message_request (SendMessageRequest): Fully validated A2A request object.

        Returns:
            SendMessageResponse: Structured response from the remote agent.
        """
        return await self.client.send_message(message_request)


# ============================================================
# ElonAgent (Host / Orchestration Layer)
# ============================================================
class ElonAgent:
    """
    Orchestration agent responsible for coordinating badminton sessions
    across multiple remote agents.

    High-Level Responsibilities:
    - Configure the LLM backend
    - Discover and register remote agents
    - Expose operational tools
    - Coordinate multi-agent workflows
    """

    def __init__(self, remote_agent_urls: Optional[List[str]] = None) -> None:
        """
        Initialize the orchestration agent configuration.

        Args:
            remote_agent_urls (Optional[List[str]]):
                Collection of remote A2A service endpoints.
        """
        # Remote agent endpoints to connect during initialization
        self.remote_agent_urls: List[str] = remote_agent_urls or []

        # Mapping: agent_name → RemoteAgentConnection instance
        self.remote_connections: Dict[str, RemoteAgentConnection] = {}

        # Mapping: agent_name → AgentCard metadata
        self.cards: Dict[str, AgentCard] = {}

        # Google ADK Agent instance (created during async setup)
        self.agent: Optional[Agent] = None

        # LLM backend configuration (Groq-hosted LLaMA model via LiteLLM)
        self.model = LiteLlm(
            model="groq/openai/gpt-oss-120b",
            temperature=0.1,
            max_tokens=400,
            reasoning_format="parsed"
        )

    async def create_agent(self) -> Agent:
        """
        Build and configure the Google ADK Agent instance.

        Initialization Workflow:
        1. Discover remote agents
        2. Establish A2A connections
        3. Register tools and orchestration instructions
        4. Return a fully configured agent

        Returns:
            Agent: Ready-to-use orchestration agent.
        """
        # Establish remote agent connections
        await self._load_remote_agents()

        # Create ADK Agent with model, metadata, and tool registry
        self.agent = Agent(
            model=self.model,
            name="elon_agent",
            description="Coordinates badminton games across connected agents.",
            instruction=self._get_instruction(),
            tools=[
                self.send_message,           # Enables inter-agent messaging
                book_badminton_court,        # Handles court booking workflow
                list_court_availabilities,   # Retrieves available time slots
            ],
        )

        return self.agent

    def _get_instruction(self):
        """
        Generate dynamic system-level instructions for the orchestration agent.

        The instruction includes:
        - Operational objectives
        - Connected agent list
        - Runtime date context
        """
        friends = "\n".join([card.name for card in self.cards.values()]) or "No connected agents"

        return f"""
        You are the Host Agent responsible for organizing badminton games.

        Operational Objectives:
        - Collect availability from connected agents (starting tomorrow).
        - Determine a mutually compatible time slot.
        - Verify court availability.
        - Confirm and book the court.

        Connected Agents:
        {friends}

        Runtime Context (Current Date):
        {datetime.datetime.now()}
        """

    async def _load_remote_agents(self):
        """
        Discover remote agents and initialize communication channels.

        Process:
        - Resolve AgentCard metadata via A2ACardResolver
        - Establish RemoteAgentConnection instances
        - Register metadata and active connections
        """
        async with httpx.AsyncClient(timeout=30) as client:
            for url in self.remote_agent_urls:
                resolver = A2ACardResolver(client, url)
                card = await resolver.get_agent_card()

                # Store metadata and connection for orchestration usage
                self.remote_connections[card.name] = RemoteAgentConnection(card, url)
                self.cards[card.name] = card

    async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
        """
        Send a task request to a connected remote agent.

        Args:
            agent_name (str): Identifier of the target agent.
            task (str): Task description or message content.
            tool_context (ToolContext): Execution context provided by ADK.

        Returns:
            SendMessageResponse: Response returned by the remote agent.
        """
        connection = self.remote_connections.get(agent_name)
        if not connection:
            raise ValueError(f"No such agent registered: {agent_name}")

        # Generate unique correlation ID for traceability
        message_id = str(uuid.uuid4())

        # Construct A2A-compliant payload structure
        payload = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": task}],
                "messageId": message_id,
            }
        }

        # Create validated A2A request object
        request = SendMessageRequest(
            id=message_id,
            params=MessageSendParams.model_validate(payload)
        )

        # Dispatch request and await response
        response = await connection.send_message(request)

        print(f"[INFO] Message dispatched successfully to {agent_name}")
        return response


# ============================================================
# Application Bootstrap
# ============================================================
async def setup():
    """
    Bootstrap the orchestration environment.

    Steps:
    1. Define remote agent endpoints
    2. Instantiate the orchestration controller
    3. Perform asynchronous initialization
    4. Return the configured agent instance
    """
    friend_urls = [
        "http://localhost:10004",
        "http://localhost:10005"
    ]

    print("Initializing Host Agent...")
    host = ElonAgent(remote_agent_urls=friend_urls)

    agent = await host.create_agent()

    print("Host Agent successfully initialized.")
    return agent


# Application entry point
# Initializes the root orchestration agent within the asyncio event loop
root_agent = asyncio.run(setup())
