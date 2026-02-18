# ============================================
# Step 2: Agent Executor (A2A Integration Layer)
# ============================================

# Import core A2A execution components
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue

# Task lifecycle management utility
from a2a.server.tasks import TaskUpdater

# Types used for structured output artifacts
from a2a.types import Part, TextPart

# Import the previously created JeffAgent
from agent import JeffAgent


# ============================================
# JeffAgentExecutor Class
# ============================================

class JeffAgentExecutor(AgentExecutor):
    """
    JeffAgentExecutor acts as the execution bridge between:
    - The A2A protocol server
    - The JeffAgent (LLM-based scheduling agent)

    It manages:
    - Task lifecycle (submit → start → complete)
    - Communication with the event queue
    - Formatting and returning structured artifacts
    """

    def __init__(self):
        """
        Initialize the executor by instantiating the JeffAgent.
        This agent handles the core AI logic.
        """
        self.agent = JeffAgent()

    # ============================================
    # Main Execution Method
    # ============================================

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """
        Executes the scheduling task when triggered by the A2A server.

        Parameters:
        - context (RequestContext): Contains user input, task metadata,
                                    thread context, and execution details.
        - event_queue (EventQueue): Used to push lifecycle updates and artifacts.
        """

        # Create a TaskUpdater to manage task lifecycle state
        # (submit → start_work → add_artifact → complete)
        updater = TaskUpdater(
            event_queue,
            context.task_id,
            context.context_id
        )

        # If task has not yet been registered, submit it
        if not context.current_task:
            await updater.submit()

        # Mark task as started
        await updater.start_work()

        # --------------------------------------------
        # Extract User Query & Context
        # --------------------------------------------

        # Retrieve user input from request context
        query = context.get_user_input()

        # Use context_id to maintain conversation memory
        context_id = context.context_id

        # --------------------------------------------
        # Call AI Agent
        # --------------------------------------------

        # Get AI-generated scheduling response
        response = await self.agent.get_response(
            query=query,
            context_id=context_id
        )

        # --------------------------------------------
        # Create Structured Artifact
        # --------------------------------------------

        # Wrap the agent's response inside A2A-compatible Part/TextPart
        parts = [
            Part(
                root=TextPart(text=response["content"])
            )
        ]

        # Add result artifact to the task output
        await updater.add_artifact(
            parts,
            name="scheduling_result"
        )

        # Mark task as completed
        await updater.complete()

    # ============================================
    # Cancel Method (Optional)
    # ============================================

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        """
        Handles task cancellation requests.

        Currently not implemented.
        In production, this could:
        - Stop long-running processes
        - Update task state to 'cancelled'
        - Clean up resources
        """
        return
