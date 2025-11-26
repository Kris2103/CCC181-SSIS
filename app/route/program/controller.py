from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import program_models, college_models

program_bp = Blueprint("program", __name__, template_folder="../../templates")

@program_bp.route("/")
def programs():
    """Display all programs and colleges."""
    programs_list = program_models.get_all()
    colleges_list = college_models.get_all()
    return render_template("programs.html", programs=programs_list, colleges=colleges_list)

@program_bp.route("/add", methods=["POST"])
def add_program():
    """Handle adding a new program."""
    code = request.form.get("program_code", "").strip()
    name = request.form.get("program_name", "").strip()
    college_code = request.form.get("college_code")
    
    try:
        program_models.create(code, name, college_code)
        flash("Program added successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")
        
    return redirect(url_for("program.programs"))

@program_bp.route("/edit", methods=["POST"])
def edit_program():
    """Handle editing an existing program."""
    
    # --- DEBUGGING STEP ---
    print("--- EDIT ROUTE ---")
    print("Received form data:", request.form)
    # ----------------------

    original_code = request.form.get("original_code")
    new_code = request.form.get("program_code", "").strip()
    new_name = request.form.get("program_name", "").strip()
    new_college = request.form.get("college_code")
    
    try:
        program_models.update(original_code, new_code, new_name, new_college)
        flash("Program updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")
        
    return redirect(url_for("program.programs"))

@program_bp.route("/delete", methods=["POST"])
def delete_program():
    """Handle deleting a program."""
    
    # --- DEBUGGING STEP ---
    print("--- DELETE ROUTE ---")
    print("Received form data:", request.form)
    # ----------------------

    code = request.form.get("program_code")
    program_models.delete(code)
    flash("Program deleted successfully!", "success")
    return redirect(url_for("program.programs"))