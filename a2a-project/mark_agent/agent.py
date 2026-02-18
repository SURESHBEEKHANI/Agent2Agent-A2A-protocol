"""
MarkAgent Module
----------------
This module defines the MarkAgent class, responsible for handling 
scheduling-related queries using CrewAI, Google's Gemini LLM, and 
a custom AvailabilityTool.
"""

# ============================================================
# Standard Library Imports
# ============================================================
import os
from dotenv import load_dotenv
import asyncio

# ============================================================
# Third-Party Library Imports
# ============================================================
from crewai import LLM, Agent, Crew, Process, Task
from langchain_groq import ChatGroq

# ============================================================
# Local Imports
# ============================================================
from tools import AvailabilityTool

# Load environment variables from a .env file
load_dotenv()


class MarkAgent:
    """
    MarkAgent handles scheduling and availability queries for Mark.

    Responsibilities:
        - Initialize and configure the Gemini LLM
        - Create a scheduling-focused AI agent
        - Process user queries through CrewAI workflow
        - Return structured availability responses
    """

    # Supported response content types
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        """
        Initialize the MarkAgent instance.

        Steps:
            1. Retrieve the Google API key from environment variables.
            2. Configure the Gemini LLM.
            3. Create the scheduling assistant agent with necessary tools.
        """
        # Retrieve API key from environment variables
        self.api_key = os.getenv("Groq_API_KEY")
        if not self.api_key:
            raise ValueError("Groq_API_KEY not found in environment variables.")

        # Initialize the Gemini LLM for scheduling tasks
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
            api_key=self.api_key
        )

        # Configure the scheduling assistant agent
        self.agent = Agent(
            role="Scheduling Assistant",
            goal="Provide accurate answers about Mark's availability.",
            backstory=(
                "You are a professional scheduling assistant responsible "
                "for checking Mark's calendar and responding clearly."
            ),
            tools=[AvailabilityTool()],  # Custom tool for calendar checks
            llm=self.llm,
        )

    async def invoke(self, user_question: str) -> str:
        """
        Process a scheduling query asynchronously.

        Args:
            user_question (str): The scheduling query from the user.

        Returns:
            str: A clear response regarding Mark's availability.
        """
        try:
            # Define the task for the agent
            task = Task(
                description=f"Answer this question: '{user_question}'",
                expected_output="A clear and concise answer about Mark's availability.",
                agent=self.agent,
            )

            # Create a Crew to execute the task sequentially
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                process=Process.sequential,
            )

            # Execute the Crew workflow
            result = await crew.kickoff()  # Make sure kickoff is awaited if async

            # Return the result as a string
            return str(result) if result else "No response available."

        except Exception as e:
            # Log error for debugging purposes
            print(f"[ERROR] MarkAgent.invoke: {e}")

            # Return a user-friendly error message
            return "Sorry, an error occurred while processing your request."


# ----------------------------------------------------
# Example Usage (For Testing Purposes Only)
# ----------------------------------------------------
# if __name__ == "__main__":
#     mark_agent = MarkAgent()
#     response = asyncio.run(
#         mark_agent.invoke("Is Mark available on 14th November 2025?")
#     )
#     print(response)
