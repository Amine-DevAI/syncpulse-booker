from langchain_core.tools import tool
from src.db.connection import reserve_slot_by_id


@tool
def make_reservation(slot_id: int, client_name: str, client_email: str) -> str:
    """Reserves an available slot using its unique slot ID and client details.

    Args:
        slot_id: The integer ID of the slot to book (e.g., 1).
        client_name: Full name of the client making the booking.
        client_email: Contact email address for the client.
    """
    try:
        success = reserve_slot_by_id(slot_id, client_name, client_email)
        if success:
            return f"Successfully reserved slot #{slot_id} for {client_name} ({client_email})."
        return f"Slot #{slot_id} is either invalid or already booked."
    except Exception as e:
        return f"Database error during reservation: {str(e)}"