from app.database import get_db
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

def create(username, email, password):
    """Creates a new user with a separate username and email."""
    hashed_password = generate_password_hash(password)
    
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);",
            (username, email, hashed_password)
        )
        conn.commit()
    finally:
        cur.close()

def get_by_email(email):
    """Fetches a user by their email address (for login)."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def get_by_username(username):
    """Fetches a user by their username (for checking during registration)."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()
    cur.close()
    return user

def check_password(stored_hash, provided_password):
    """Checks if a provided password matches the stored hash."""
    return check_password_hash(stored_hash, provided_password)