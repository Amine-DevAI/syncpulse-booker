import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "book_data")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Build connection URL (handles empty password cleanly)
if DB_PASSWORD:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def query_available_slots(date_str: str) -> list[dict]:
    """Queries available booking slots for a target date (YYYY-MM-DD)."""
    sql = text("""
        SELECT id, start_time, end_time, status 
        FROM slots 
        WHERE booking_date = :date AND status = 'available'
        ORDER BY start_time ASC
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {"date": date_str})
        return [
            {
                "id": row.id,
                "start_time": str(row.start_time),
                "end_time": str(row.end_time),
                "status": row.status,
            }
            for row in result
        ]


if __name__ == "__main__":
    print("Testing connection against book_data container...")
    try:
        slots = query_available_slots("2026-09-10")
        print(f"Success! Retrieved slots: {slots}")
    except Exception as e:
        print(f"Database connection failed: {e}")





def reserve_slot_by_id(slot_id: int, client_name: str, client_email: str) -> bool:
    """Marks a specific slot as 'booked' and attaches client details."""
    sql = text("""
        UPDATE slots
        SET status = 'booked', client_name = :name, client_email = :email
        WHERE id = :slot_id AND status = 'available'
    """)
    with engine.begin() as conn:
        result = conn.execute(
            sql,
            {"slot_id": slot_id, "name": client_name, "email": client_email},
        )
        # Returns True if a row was actually updated
        return result.rowcount > 0