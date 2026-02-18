# ==============================
# Imports
# ==============================
import os
import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages.ai import AIMessage
from langchain_groq import ChatGroq
from tools import get_availability

# ==============================
# Step 1: Load Environment & Setup Memory
# ==============================
load_dotenv()  # Load environment variables (e.g., API keys)

# Retrieve and set API keys securely
Groq_API_KEY = os.getenv("Groq_API_KEY")
os.environ["Groq_API_KEY"] = Groq_API_KEY

# Initialize memory for conversation history
memory = MemorySaver()

# ==============================
# JeffAgent Class
# ==============================
class JeffAgent:
    """
    JeffAgent: AI assistant for scheduling Jeff Bezos's badminton sessions.

    Responsibilities:
    - Use only the 'get_availability' tool.
    - Politely refuse unrelated questions.
    """

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        """Initialize model, tools, system prompt, and agent graph with memory."""

        # Initialize Groq model (ChatGroq)
        self.model = ChatGroq(
            model="qwen/qwen3-32b",
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2
        )

        # Register tools (if available)
        self.tools = [get_availability] if get_availability else []

        # System prompt to control agent behavior
        self.system_prompt = """
Jeff Bezos's personal scheduling assistant.

Responsibilities:
- Use the 'get_availability' tool to answer questions about 
  Jeff Bezos's badminton schedule.

Behavior:
- Politely refuse questions unrelated to badminton scheduling.
- Suggest asking about available times instead.
- Keep responses concise, professional, and friendly.
"""

        # Create LangGraph agent with memory checkpointing
        self.graph = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=memory
        )

    # ==============================
    # Async Method: Get Response
    # ==============================
    async def get_response(self, query: str, context_id) -> dict:
        """
        Generate a response from the agent.

        Args:
            query (str): User input question.
            context_id (str/int): Unique conversation thread ID.

        Returns:
            dict: {"content": <response_text>}
        """

        # Prepare input and configuration for LangGraph
        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": context_id}}

        # Invoke the agent graph
        raw_response = self.graph.invoke(inputs, config)

        # Extract AI messages
        messages = raw_response.get("messages", [])
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]

        if not ai_messages:
            return {"content": "No response"}

        # Use the latest AI message
        content = ai_messages[-1]

        # Handle structured or plain text responses
        if isinstance(content, list):
            response = " ".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            )
        else:
            response = str(content)

        return {"content": response}


# ==============================
# Example Usage
# ==============================
#if __name__ == "__main__":
#    agent = JeffAgent()
#    response = asyncio.run(
#        agent.get_response("Is Jeff available on 8th Nov 2025?", context_id=1234)
#    )
#    print(response)
