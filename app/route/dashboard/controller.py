from flask import Blueprint, render_template
from app.models import student_models, program_models, college_models # Adjust imports as needed
import json

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    """
    Gathers all data needed for the dashboard and renders the template.
    """
    # Get total counts
    total_students = student_models.count()
    total_programs = program_models.count()
    total_colleges = college_models.count()

    # Get data for "Students by Program" bar chart
    students_by_program = student_models.get_count_by_program()
    program_labels = [item['program_code'] for item in students_by_program]
    program_data = [item['count'] for item in students_by_program]
    
    # Get data for "Gender Distribution" pie chart
    gender_distribution = student_models.get_count_by_gender()
    gender_labels = [item['gender'] for item in gender_distribution]
    gender_data = [item['count'] for item in gender_distribution]

    latest_students = student_models.get_latest(5)

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges,
        # Use json.dumps to safely pass data to the template for JavaScript
        program_labels=json.dumps(program_labels),
        program_data=json.dumps(program_data),
        gender_labels=json.dumps(gender_labels),
        gender_data=json.dumps(gender_data),
        latest_students=latest_students
    )