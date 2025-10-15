from app.database import get_db
import psycopg2.extras

class Program:
    """A simple data container for a program."""
    def __init__(self, program_code, program_name, college_code, **kwargs):
        self.program_code = program_code
        self.program_name = program_name
        self.college_code = college_code

# --- Module-level functions handle all logic ---

def get_all():
    """Fetches all programs, joining with college names for display."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT p.program_code, p.program_name, p.college_code, c.college_name
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code
        ORDER BY p.program_code;
    """)
    programs = cur.fetchall()
    cur.close()
    return programs

def all():
    """Alias for get_all (used by controllers/templates)."""
    return get_all()

def get_by_code(code):
    """Fetches a single program by its code."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM programs WHERE program_code = %s;", (code,))
    program = cur.fetchone()
    cur.close()
    return program

def get(code):
    """Alias for get_by_code (for easy imports)."""
    return get_by_code(code)

def create(program_code, program_name, college_code):
    """Creates a new program with validation."""
    if not program_code or not program_name or not college_code:
        raise ValueError("All fields are required.")
    if get_by_code(program_code):
        raise ValueError(f"Program code '{program_code}' already exists.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO programs (program_code, program_name, college_code) VALUES (%s, %s, %s);",
        (program_code, program_name, college_code)
    )
    conn.commit()
    cur.close()

def update(original_code, new_code, new_name, new_college):
    """Updates a program with validation."""
    if not new_code or not new_name or not new_college:
        raise ValueError("All fields are required.")
    if original_code != new_code and get_by_code(new_code):
        raise ValueError(f"Program code '{new_code}' already exists.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE programs 
        SET program_code = %s, program_name = %s, college_code = %s
        WHERE program_code = %s;
    """, (new_code, new_name, new_college, original_code))
    conn.commit()
    cur.close()

def delete(code):
    """Deletes a program by its code."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM programs WHERE program_code = %s;", (code,))
    conn.commit()
    cur.close()
    return True

def count():
    """Returns the total number of programs."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM programs;")
    total = cur.fetchone()[0]
    cur.close()
    return total