# ==============================
# Step 1: Agent & Tool
# ==============================

# A mock dictionary representing Mark's availability on certain dates.
# Key: date in 'YYYY-MM-DD' format
# Value: availability status as a string
FAKE_AVAILABILITY = {
    "2026-02-19": "Available from 11:00 AM to 03:00 PM",
    "2026-02-20": "Available all day",
    "2026-02-21": "Busy all day",
    "2026-02-22": "Available from 10:00 AM to 02:00 PM",
    "2026-02-23": "Available all day",
}


def get_availability(date_str: str) -> dict[str, str]:
    """
    Simulates checking Mark's availability for a specific date.

    Args:
        date_str (str): The date to check in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary with 'status' and 'message' describing availability.
              - status: 'completed', 'input_required', or 'error'
              - message: human-readable information about availability
    """

    # Handle missing input
    if not date_str:
        return {"status": "error", "message": "No date provided."}

    # Look up availability in the mock dictionary
    availability = FAKE_AVAILABILITY.get(date_str)

    # If availability is found, return it with a completed status
    if availability:
        return {
            "status": "completed",
            "message": f"On {date_str}, Jeff is {availability}.",
        }

    # If date not found, ask user to check another date
    return {
        "status": "input_required",
        "message": f"He is not available on {date_str}. Please ask about another date.",
    }

# Import BaseTool from crewai.tools to create custom tools
from crewai.tools import BaseTool


class AvailabilityTool(BaseTool):
    """
    A tool class to integrate with the agent system.
    This tool uses get_availability to check Mark's availability for a given date.
    """

    # Name of the tool
    name: str = "Calendar Availability Checker"

    # Short description of what the tool does
    description: str = "Checks Mark's availability for a given date."

    def _run(self, date: str) -> str:
        """
        Executes the tool logic for the given date.

        Args:
            date (str): The date to check availability.

        Returns:
            str: The message returned by get_availability.
        """
        return get_availability(date)["message"]
