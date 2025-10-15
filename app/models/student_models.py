from app.database import get_db
import psycopg2.extras

class Student:
    """Data container for a student."""
    def __init__(self, id_number, first_name, last_name, gender, year_level, program_code, **kwargs):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year_level = year_level
        self.program_code = program_code

# --- Module-level functions ---

def get_all():
    """Fetch all students (minimal info)."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id_number, first_name, last_name, gender, year_level, program_code
        FROM students
        ORDER BY id_number;
    """)
    students = cur.fetchall()
    cur.close()
    return students

def get_by_id(id_number):
    """Fetch single student by id_number."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id_number, first_name, last_name, gender, year_level, program_code
        FROM students
        WHERE id_number = %s;
    """, (id_number,))
    student = cur.fetchone()
    cur.close()
    return student

def get(id_number):
    """Alias for get_by_id (for easy imports)."""
    return get_by_id(id_number)

def create(id_number, first_name, last_name, gender, year_level, program_code):
    """Creates a new student with validation."""
    # Use Python's built-in 'all', NOT a model-level 'all'
    if not all([id_number, first_name, last_name, gender, year_level, program_code]):
        raise ValueError("All fields are required.")
    if get_by_id(id_number):
        raise ValueError(f"ID number '{id_number}' already exists.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (id_number, first_name, last_name, gender, year_level, program_code)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (id_number, first_name, last_name, gender, year_level, program_code))
    conn.commit()
    cur.close()

def update(id_number, first_name=None, last_name=None, gender=None, year_level=None, program_code=None):
    """Updates a student by id_number."""
    if not get_by_id(id_number):
        raise ValueError("Student does not exist.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET first_name = COALESCE(%s, first_name),
            last_name = COALESCE(%s, last_name),
            gender = COALESCE(%s, gender),
            year_level = COALESCE(%s, year_level),
            program_code = COALESCE(%s, program_code)
        WHERE id_number = %s;
    """, (first_name, last_name, gender, year_level, program_code, id_number))
    conn.commit()
    cur.close()

def delete(id_number):
    """Deletes a student by id_number."""
    print("DEBUG: ID to delete:", repr(id_number))
    # Print all student IDs
    existing_students = get_all()
    ids = [s['id_number'] for s in existing_students]
    print("DEBUG: All IDs in DB:", ids)
    result = get_by_id(id_number)
    print("DEBUG: get_by_id result:", result)
    if not result:
        raise ValueError("Student does not exist.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id_number = %s;", (id_number,))
    conn.commit()
    cur.close()
    return True

def count():
    """Returns the total number of students."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students;")
    # fetchone() returns a tuple like (15,), so we get the first element
    total = cur.fetchone()[0]
    cur.close()
    return total

def get_count_by_program():
    """Returns the count of students for each program."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT program_code, COUNT(*) as count
        FROM students
        GROUP BY program_code
        ORDER BY count DESC;
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_count_by_gender():
    """Returns the count of students for each gender."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT gender, COUNT(*) as count
        FROM students
        GROUP BY gender;
    """)
    result = cur.fetchall()
    cur.close()
    return result

def get_latest(limit):
    """
    Fetches the most recently added students, up to a given limit.
    NOTE: This assumes you have a 'created_at' timestamp column.
    If not, you can ORDER BY another column like 'id_number'.
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT id_number, first_name, last_name, program_code, year_level
        FROM students
        ORDER BY id_number DESC
        LIMIT %s;
    """, (limit,))
    students = cur.fetchall()
    cur.close()
    return students
