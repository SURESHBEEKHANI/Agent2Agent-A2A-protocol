# ============================================
# 🗓️ Mock Calendar Data (Simulated Schedule)
# ============================================

# This dictionary simulates Jeff's badminton availability.
# In a real-world production system, this would be replaced
# with a database query or Google Calendar API integration.
FAKE_AVAILABILITY = {
    "2025-11-09": "Available from 4:00 PM to 6:00 PM",
    "2025-11-10": "Available from 10:00 AM to 12:00 PM",
    "2025-11-11": "Available from 11:00 AM to 12:00 PM",
    "2025-11-12": "Busy all afternoon (1:00 PM – 5:00 PM)",
    "2025-11-13": "Available all day",
}


# ============================================
# Tool Function: get_availability
# ============================================

def get_availability(date_str: str) -> dict[str, str]:
    """
    Simulates checking Jeff's availability on a specific date.

    This function acts as a tool that can be called by an AI agent.
    It looks up the provided date in the FAKE_AVAILABILITY dictionary
    and returns a structured response.

    Args:
        date_str (str):
            Date string in 'YYYY-MM-DD' format.

    Returns:
        dict[str, str]:
            A structured dictionary containing:
            - status: Indicates result type
                • "completed"       → Valid availability found
                • "input_required"  → Date not available
                • "error"           → Invalid or missing input
            - message: Human-readable response
    """

    # --------------------------------------------
    # Input Validation
    # --------------------------------------------

    # If no date is provided, return an error response
    if not date_str:
        return {
            "status": "error",
            "message": "No date provided."
        }

    # --------------------------------------------
    # Availability Lookup
    # --------------------------------------------

    # Attempt to retrieve availability from mock calendar
    availability = FAKE_AVAILABILITY.get(date_str)

    # --------------------------------------------
    # Successful Match
    # --------------------------------------------

    # If availability exists for the given date,
    # return a completed status with formatted message
    if availability:
        return {
            "status": "completed",
            "message": f"On {date_str}, Jeff is {availability}.",
        }

    # --------------------------------------------
    # No Availability Found
    # --------------------------------------------

    # If date is not found in calendar,
    # request user to provide another date
    return {
        "status": "input_required",
        "message": f"He is not available on {date_str}. Please ask about another date.",
    }
