from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import college_models

college_bp = Blueprint("college", __name__, template_folder="../../templates")

@college_bp.route("/")
def colleges():
    """Display all colleges."""
    colleges_list = college_models.get_all()
    return render_template("colleges.html", colleges=colleges_list)

@college_bp.route("/add", methods=["POST"])
def add_college():
    """Handle the creation of a new college."""
    code = request.form.get("college_code", "").strip()
    name = request.form.get("college_name", "").strip()

    try:
        college_models.create(college_code=code, college_name=name)
        flash("College added successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")
        
    return redirect(url_for("college.colleges"))

@college_bp.route("/edit", methods=["POST"])
def edit_college():
    """Handle updates to an existing college."""
    original_code = request.form.get("original_college_code")
    new_code = request.form.get("college_code", "").strip()
    new_name = request.form.get("college_name", "").strip()

    try:
        college_models.update(
            original_code=original_code, 
            new_code=new_code, 
            new_name=new_name
        )
        flash("College updated successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("college.colleges"))

@college_bp.route("/delete", methods=["POST"])
def delete_college():
    """Handle the deletion of a college."""
    code_to_delete = request.form.get("college_code")
    
    college_models.delete(code=code_to_delete)
    flash("College deleted successfully!", "success")
        
    return redirect(url_for("college.colleges"))