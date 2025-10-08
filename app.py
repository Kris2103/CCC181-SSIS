from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get database credentials from .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )
    return conn


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.program_name, COUNT(s.id_number) AS total_students
        FROM programs p
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY p.program_name
        ORDER BY total_students DESC
        LIMIT 5;
    """)
    top_programs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("dashboard.html", top_programs=top_programs, enumerate=enumerate)


@app.route("/students")
def students():
    conn = get_db_connection()
    # use RealDictCursor so results come as dictionaries
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT s.id_number AS id,
               s.first_name AS firstname,
               s.last_name AS lastname,
               p.program_name AS course,
               s.year_level AS year,
               s.gender
        FROM students s
        LEFT JOIN programs p ON s.program_code = p.program_code
        ORDER BY s.id_number
    """)

    students = cur.fetchall()  # already a list of dictionaries

    cur.close()
    conn.close()

    return render_template("students.html", students=students)


@app.route("/programs")
def programs():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.program_code,
            p.program_name,
            c.college_code,
            c.college_name
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code
        ORDER BY p.program_code;
    """)

    rows = cur.fetchall()
    conn.close()

    programs = [
        {
            "program_code": r["program_code"],
            "program_name": r["program_name"],
            "college_code": r["college_code"],
            "college_name": r["college_name"] if r["college_name"] else "N/A"
        }
        for r in rows
    ]

    return render_template("programs.html", programs=programs)



@app.route("/colleges")
def colleges():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT 
            college_code AS code,
            college_name AS name
        FROM colleges
        ORDER BY college_code
    """)

    colleges = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("colleges.html", colleges=colleges)

if __name__ == "__main__":
    app.run(debug=True)
