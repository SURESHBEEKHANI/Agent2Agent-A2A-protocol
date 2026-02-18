# ============================================================
# Dummy Greeting Agent Implementation
# This module demonstrates a minimal async agent and its
# corresponding A2A AgentExecutor integration.
# ============================================================

import asyncio


class GreetingAgent:
    """
    A simple asynchronous greeting agent.

    This agent is designed for demonstration and testing purposes.
    It exposes an async `invoke` method that returns a static
    greeting message.

    In a real-world scenario, this method could contain:
    - LLM calls
    - Business logic
    - API integrations
    - Database interactions
    """

    async def invoke(self) -> str:
        """
        Execute the agent's primary logic.

        Returns:
            str: A greeting message.
        """
        return "Hi Everyone! Welcome to AI with SURESH BEEKHANI."


# ============================================================
# A2A Agent Executor Integration
# ============================================================

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message


class GreetingAgentExecutor(AgentExecutor):
    """
    AgentExecutor implementation for the GreetingAgent.

    This class acts as a bridge between the A2A framework
    and the GreetingAgent. It handles execution lifecycle
    events such as execution and cancellation.
    """

    def __init__(self):
        """
        Initialize the executor with an instance
        of the GreetingAgent.
        """
        self.agent = GreetingAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """
        Execute the GreetingAgent and enqueue its response.

        Args:
            context (RequestContext): Metadata and request information
                                      provided by the A2A framework.
            event_queue (EventQueue): Queue used to send events/messages
                                      back to the client or orchestrator.
        """
        # Invoke the agent's main logic
        result = await self.agent.invoke()

        # Wrap the result in an A2A-compatible message format
        # and enqueue it for downstream processing
        await event_queue.enqueue_event(new_agent_text_message(result) )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        """
        Handle cancellation requests.

        Currently, cancellation is not supported for this agent.

        Raises:
            Exception: Indicates cancellation is unsupported.
        """
        raise Exception("Cancel not supported")


# ============================================================
# Optional Standalone Test Execution
# (Used for local debugging outside A2A framework)
# ============================================================

"""
async def main():
    agent = GreetingAgent()
    greeting = await agent.invoke()
    print(greeting)

if __name__ == "__main__":
    asyncio.run(main())
"""
