from langchain_core.tools import tool
from src.db.connection import query_available_slots


@tool
def check_availability(date: str) -> str:
    """Checks the booking database for open slots on a specific date.

    Args:
        date: Target date string in YYYY-MM-DD format.
    """
    try:
        slots = query_available_slots(date)
        if not slots:
            return f"No open slots available for {date}."

        formatted_slots = [
            f"Slot #{s['id']}: {s['start_time']} - {s['end_time']}"
            for s in slots
        ]
        return f"Available slots on {date}:\n" + "\n".join(formatted_slots)
    except Exception as e:
        return f"Database error while querying slots: {str(e)}"