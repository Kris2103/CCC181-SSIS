from app.database import get_db
import psycopg2.extras
import os
from config import supabase, SUPABASE_BASE_URL, STORAGE_BUCKET 

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEFAULT_AVATAR_FILENAME = 'default_student_avatar.png'

class Student:
    """Data container for a student."""
    def __init__(self, id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url=None, **kwargs):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year_level = year_level
        self.program_code = program_code
        self.profile_picture_url = profile_picture_url

def _construct_full_url(relative_path):
    """
    Prepends the Supabase base URL if the path is relative (i.e., not already a full URL).
    This handles both custom photos and the default avatar.
    """
    # If the path is None, empty, or already a full external URL, return it as is.
    if not relative_path or relative_path.startswith('http'):
        return relative_path
        
    # If the path is any relative path (like 'default_student_avatar.png' or '2024-0001.jpg'), prepend the full base URL.
    return SUPABASE_BASE_URL + relative_path

def _clean_url_to_path(full_url):
    """Converts the full public URL back to the relative path stored in the DB."""
    if full_url and full_url.startswith(SUPABASE_BASE_URL):
        return full_url.replace(SUPABASE_BASE_URL, '')
    return full_url

def is_allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_profile_picture(id_number, file):
    """Uploads a profile picture to Supabase Storage."""
    if file and is_allowed_file(file.filename):
        filename = f"{id_number}_{file.filename}".replace(" ", "_")
        file_bytes = file.read()

        # Upload to Supabase Storage
        supabase.storage.from_(STORAGE_BUCKET).upload(
            path=filename,
            file=file_bytes,
            file_options={"content-type": "image/*"}
        )

        return filename  # this is saved in PostgreSQL (relative path)

    return None

# --- Module-level functions ---

def get_all():
    """Fetch all students (minimal info)."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url
        FROM students
        ORDER BY id_number;
    """)
    students = cur.fetchall()
    cur.close()

    for student in students:
        student['profile_picture_url'] = _construct_full_url(student.get('profile_picture_url'))

    return students

def get_by_id(id_number):
    """Fetch single student by id_number."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url
        FROM students
        WHERE id_number = %s;
    """, (id_number,))
    student = cur.fetchone()
    cur.close()
    
    if student:
        student['profile_picture_url'] = _construct_full_url(student.get('profile_picture_url'))

    return student

def get(id_number):
    """Alias for get_by_id (for easy imports)."""
    return get_by_id(id_number)

def create(id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url=None):
    """Creates a new student with validation."""
    # Use Python's built-in 'all', NOT a model-level 'all'
    if not all([id_number, first_name, last_name, gender, year_level, program_code]):
        raise ValueError("All fields are required.")
    if get_by_id(id_number):
        raise ValueError(f"ID number '{id_number}' already exists.")
    
    stored_path = _clean_url_to_path(profile_picture_url).lstrip("/") if profile_picture_url else DEFAULT_AVATAR_FILENAME

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (id_number, first_name, last_name, gender, year_level, program_code, stored_path))
    conn.commit()
    cur.close()

def update(id_number, first_name=None, last_name=None, gender=None, year_level=None, program_code=None, profile_picture_url=None):
    """Updates a student by id_number."""
    if not get_by_id(id_number):
        raise ValueError("Student does not exist.")
    
    stored_path = _clean_url_to_path(profile_picture_url).lstrip("/") if profile_picture_url else DEFAULT_AVATAR_FILENAME

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET first_name = COALESCE(%s, first_name),
            last_name = COALESCE(%s, last_name),
            gender = COALESCE(%s, gender),
            year_level = COALESCE(%s, year_level),
            program_code = COALESCE(%s, program_code),
            profile_picture_url = COALESCE(%s, profile_picture_url)
        WHERE id_number = %s;
    """, (first_name, last_name, gender, year_level, program_code, stored_path, id_number))
    conn.commit()
    cur.close()

def delete(id_number):
    """Deletes a student by id_number, and removes the associated file from Supabase Storage."""
    conn = get_db()
    
    # We use a dictionary cursor here to easily access the column name.
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
    
    # Select the profile_picture_url column
    cur.execute("SELECT profile_picture_url FROM students WHERE id_number = %s;", (id_number,))
    result = cur.fetchone()
    
    if not result:
        cur.close()
        raise ValueError("Student does not exist.")
    
    file_path_db = result.get('profile_picture_url')
    
    # DELETE THE RECORD FROM LOCAL DB
    cur.close() 
    cur = conn.cursor() 
    cur.execute("DELETE FROM students WHERE id_number = %s;", (id_number,))
    conn.commit()
    cur.close()
    
    if supabase and file_path_db and file_path_db != DEFAULT_AVATAR_FILENAME:
        try:
            supabase.storage.from_(STORAGE_BUCKET).remove([file_path_db])
            print(f"Successfully deleted file from Supabase Storage: {file_path_db}")
        except Exception as e:
            print(f"Warning: Failed to delete file {file_path_db} from storage: {e}")
            
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
