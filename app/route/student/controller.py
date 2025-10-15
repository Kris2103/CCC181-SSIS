from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import student_models, program_models
import re

student_bp = Blueprint("student", __name__, template_folder="../../templates")

@student_bp.route("/")
def students():
    students_list = student_models.get_all()
    programs_list = program_models.all()
    return render_template("students.html", students=students_list, programs=programs_list)

@student_bp.route("/add", methods=["POST"])
def add_student():
    id_number = request.form.get("id_number").strip()
    first_name = request.form.get("first_name").strip()
    last_name = request.form.get("last_name").strip()
    gender = request.form.get("gender")
    year_level = request.form.get("year_level")
    program_code = request.form.get("program_code")

    if not all([id_number, first_name, last_name, gender, year_level, program_code]):
        flash("All fields are required.", "danger")
        return redirect(url_for("student.students"))

    if not re.match(r"^\d{4}-\d{4}$", id_number):
        flash("Invalid ID format (YYYY-NNNN).", "danger")
        return redirect(url_for("student.students"))

    if student_models.get(id_number):
        flash("ID number already exists!", "danger")
        return redirect(url_for("student.students"))

    student_models.create(id_number, first_name, last_name, gender, year_level, program_code)
    flash("Student added successfully!", "success")
    return redirect(url_for("student.students"))

@student_bp.route("/edit", methods=["POST"])
def edit_student():
    id_number = request.form.get("id_number")
    first_name = request.form.get("first_name").strip()
    last_name = request.form.get("last_name").strip()
    gender = request.form.get("gender")
    year_level = request.form.get("year_level")
    program_code = request.form.get("program_code")

    # Check if program exists before updating
    if not program_models.get(program_code):
        flash("Selected program does not exist!", "danger")
        return redirect(url_for("student.students"))

    # Update student
    student_models.update(id_number, first_name, last_name, gender, year_level, program_code)
    flash("Student updated successfully!", "success")
    return redirect(url_for("student.students"))

@student_bp.route("/delete", methods=["POST"])
def delete_student():
    id_number = request.form.get("id_number")
    try:
        student_models.delete(id_number)
        flash("Student deleted successfully!", "success")
    except ValueError:
        flash("Student does not exist.", "danger")
    return redirect(url_for("student.students"))
