# httpx is an async HTTP client used to make API calls
import httpx

# A2A client utilities
from a2a.client import A2ACardResolver, ClientFactory, ClientConfig

# Async support
import asyncio

# A2A message-related types
from a2a.types import TransportProtocol, Message, Role, Part, TextPart

# Used to generate unique message IDs
import uuid


# Base URL where the A2A agent server is running
BASE_URL = "http://localhost:9999/"

# Standard public path where agent metadata (AgentCard) is exposed
PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"


async def main():
    """
    Main async function:
    1. Fetches the Agent Card
    2. Creates an A2A client
    3. Sends a message to the agent
    4. Prints streaming responses
    """

    # Create an async HTTP client session
    async with httpx.AsyncClient() as httpx_client:

        # -----------------------------------
        # Step 1: Resolve / Fetch Agent Card
        # -----------------------------------
        # A2ACardResolver automatically fetches:
        # http://localhost:9999/.well-known/agent.json
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL
        )

        # Retrieve the agent metadata
        agent_card = await resolver.get_agent_card()

        # Print agent metadata in formatted JSON
        print("Agent Card", agent_card.model_dump_json(indent=2))

        # -----------------------------------
        # Step 2: Create A2A Client
        # -----------------------------------
        # Define supported transport protocols
        # jsonrpc is the standard A2A communication format
        supported = [TransportProtocol.jsonrpc]

        # Client configuration (HTTP client + supported transports)
        factory = ClientFactory(
            ClientConfig(
                httpx_client=httpx_client,
                supported_transports=supported
            )
        )

        # Create a client instance using the agent's metadata
        a2a_client = factory.create(agent_card)

        print("A2A Client Initialized")

        # -----------------------------------
        # Step 3: Create Message to Send
        # -----------------------------------
        # Message represents user input in A2A format
        message = Message(
            role=Role.user,                       # Sender role (user → agent)
            message_id=str(uuid.uuid4()),         # Unique ID for tracking
            parts=[
                # TextPart contains the actual message content
                Part(root=TextPart(text="Hi How are you?"))
            ],
        )

        # -----------------------------------
        # Step 4: Send Message (Streaming)
        # -----------------------------------
        # send_message() returns an async generator
        # It streams response events from the agent
        async for event in a2a_client.send_message(message):
            
            # Print each streamed event in formatted JSON
            print("Response", event.model_dump_json(indent=2))


# Entry point for async execution
if __name__ == "__main__":
    asyncio.run(main())
