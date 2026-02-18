# ==============================
# Step 2: Agent Executor
# ==============================

# Import the base executor class for agents
from a2a.server.agent_execution import AgentExecutor

# Import RequestContext, which holds info about the current task and user input
from a2a.server.agent_execution.context import RequestContext

# EventQueue is used to send events back to the system (like task updates)
from a2a.server.events.event_queue import EventQueue

# TaskUpdater helps manage task lifecycle: submit, start, add artifacts, complete
from a2a.server.tasks import TaskUpdater

# Import the custom agent class (MarkAgent) that will handle user queries
from agent import MarkAgent

# Types for structuring the agent's output
from a2a.types import Part, TextPart


class MarkAgentExecutor(AgentExecutor):
    """
    A custom executor for MarkAgent.
    Handles receiving a user query, invoking the agent, and updating the task workflow.
    """

    def __init__(self):
        # Instantiate the MarkAgent instance
        self.agent = MarkAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """
        Main execution method called by the agent framework.
        
        Args:
            context (RequestContext): Contains information about the current task,
                                      user input, and context IDs.
            event_queue (EventQueue): Queue for sending task events/updates.
        """

        # Initialize a TaskUpdater to manage task progress
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        # If there is no current task, submit a new one
        if not context.current_task:
            await updater.submit()
        
        # Mark the task as started
        await updater.start_work()

        # Get the user's input/query from the context
        query = context.get_user_input()

        # Invoke the agent asynchronously with the user's query
        response = await self.agent.invoke(user_question=query)

        # Wrap the agent's response in a structured Part for the system
        parts = [Part(root=TextPart(text=response))]

        # Add the response as an artifact named "scheduling_result"
        await updater.add_artifact(parts, name="scheduling_result")

        # Mark the task as complete
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        """
        Handles task cancellation.
        Currently, this method does nothing but could be extended
        to stop the agent or clean up resources if needed.
        """
        return
