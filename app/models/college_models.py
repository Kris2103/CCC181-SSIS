from app.database import get_db
import psycopg2.extras

# The class is just a simple data container.
class College:
    def __init__(self, college_code, college_name, **kwargs):
        self.college_code = college_code
        self.college_name = college_name

# --- Module-level functions handle all logic ---

def get_all():
    """Fetches all colleges from the database."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM colleges ORDER BY college_code;")
    colleges = cur.fetchall()
    cur.close()
    return colleges

def get_by_code(code):
    """Fetches a single college by its code."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM colleges WHERE college_code = %s;", (code,))
    college = cur.fetchone()
    cur.close()
    return college

def create(college_code, college_name):
    """Creates a new college with validation."""
    if not college_code or not college_name:
        raise ValueError("College code and name cannot be empty.")
    
    if get_by_code(college_code):
        raise ValueError(f"College with code '{college_code}' already exists.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO colleges (college_code, college_name) VALUES (%s, %s);",
        (college_code, college_name)
    )
    conn.commit()
    cur.close()

def update(original_code, new_code, new_name):
    """Updates a college with validation."""
    if not new_code or not new_name:
        raise ValueError("College code and name cannot be empty.")

    if original_code != new_code and get_by_code(new_code):
        raise ValueError(f"Cannot update: College code '{new_code}' is already in use.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE colleges 
        SET college_code = %s, college_name = %s
        WHERE college_code = %s;
    """, (new_code, new_name, original_code))
    conn.commit()
    cur.close()

def delete(code):
    """Deletes a college by its code."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM colleges WHERE college_code = %s;", (code,))
    conn.commit()
    cur.close()
    return True

def count():
    """Returns the total number of colleges."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM colleges;")
    total = cur.fetchone()[0]
    cur.close()
    return total