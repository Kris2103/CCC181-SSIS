from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import student_models, program_models
from config import SUPABASE_BASE_URL, STORAGE_BUCKET, supabase
from app.models.student_models import DEFAULT_AVATAR_FILENAME, is_allowed_file
import re
import time

student_bp = Blueprint("student", __name__, template_folder="../../templates")
DEFAULT_AVATAR_URL = SUPABASE_BASE_URL + DEFAULT_AVATAR_FILENAME

@student_bp.route("/")
def students():
    students_list = student_models.get_all()
    programs_list = program_models.all()

    if students_list:
        print(f"DEBUG: First student photo URL: {students_list[0].get('profile_picture_url')}")

    return render_template("students.html", students=students_list, programs=programs_list, default_avatar_url=DEFAULT_AVATAR_URL)

@student_bp.route("/add", methods=["POST"])
def add_student():
    id_number = request.form.get("id_number").strip()
    first_name = request.form.get("first_name").strip()
    last_name = request.form.get("last_name").strip()
    gender = request.form.get("gender")
    year_level = request.form.get("year_level")
    program_code = request.form.get("program_code")
    photo_file = request.files.get("photo_file")
    final_photo_db_path = None

    if not all([id_number, first_name, last_name, gender, year_level, program_code]):
        flash("All fields are required.", "danger")
        return redirect(url_for("student.students"))

    if not re.match(r"^\d{4}-\d{4}$", id_number):
        flash("Invalid ID format (YYYY-NNNN).", "danger")
        return redirect(url_for("student.students"))

    if student_models.get(id_number):
        flash("ID number already exists!", "danger")
        return redirect(url_for("student.students"))
    
    try:
        year_level_int = int(year_level)
        if not (1 <= year_level_int <= 4):
            flash("Year Level must be between 1 and 4.", "danger")
            return redirect(url_for("student.students"))
    except (ValueError, TypeError):
        flash("Year Level must be a valid number.", "danger")
        return redirect(url_for("student.students"))
    
    # Photo Upload
    if photo_file and photo_file.filename and is_allowed_file(photo_file.filename):
        try:
            extension = photo_file.filename.rsplit(".", 1)[1].lower()
            timestamp = int(time.time())  # add timestamp for uniqueness
            file_path = f"students/{id_number}_{timestamp}.{extension}"
            file_content = photo_file.read()

            if len(file_content) > 0:
                supabase.storage.from_(STORAGE_BUCKET).upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": photo_file.mimetype}
                )
                final_photo_db_path = file_path
            else:
                flash("Photo file is empty.", "warning")

        except Exception as e:
            print("UPLOAD ERROR:", e)
            flash("Error uploading photo.", "warning")

    # Create student
    student_models.create(
        id_number=id_number,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        year_level=year_level,
        program_code=program_code,
        profile_picture_url=final_photo_db_path  # None -> default used
    )
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
    photo_file = request.files.get("photo_file")
    profile_picture_url = request.form.get("profile_picture_url")

    # Check if program exists before updating
    if not program_models.get(program_code):
        flash("Selected program does not exist!", "danger")
        return redirect(url_for("student.students"))
    
    if year_level:
        try:
            year_level_int = int(year_level)
            if not (1 <= year_level_int <= 4):
                flash("Year Level must be between 1 and 4.", "danger")
                return redirect(url_for("student.students"))
        except (ValueError, TypeError):
            flash("Year Level must be a valid number.", "danger")
            return redirect(url_for("student.students"))
    
    # Handle new photo upload
    if photo_file and photo_file.filename and student_models.is_allowed_file(photo_file.filename):
        try:
            extension = photo_file.filename.rsplit(".", 1)[1].lower()
            timestamp = int(time.time())
            file_path = f"students/{id_number}_{timestamp}.{extension}"

            # Read file content
            photo_file.seek(0)
            file_content = photo_file.read()

            if len(file_content) > 0:
                # Upload new file
                supabase.storage.from_(STORAGE_BUCKET).upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": photo_file.mimetype}
                )

                # Update DB path
                profile_picture_url = file_path
            else:
                flash("Uploaded photo is empty. Keeping existing photo.", "warning")

        except Exception as e:
            print("UPLOAD ERROR:", e)
            flash("Error uploading new photo. Keeping existing photo.", "warning")


    # Update student
    student_models.update(id_number, first_name, last_name, gender, year_level, program_code, profile_picture_url=profile_picture_url)
    flash("Student updated successfully!", "success")
    return redirect(url_for("student.students"))

@student_bp.route("/upload_photo", methods=["POST"])
def upload_photo():
    """
    Handles student photo uploads using Supabase Storage service role key.
    Returns a public URL for the uploaded photo.
    """
    file = request.files.get("photo_file")
    id_number = request.form.get("id_number")

    # Validate input
    if not file or file.filename == "":
        return jsonify({"success": False, "message": "No file selected."}), 400
    if not id_number or not re.match(r"^\d{4}-\d{4}$", id_number):
        return jsonify({"success": False, "message": "Invalid or missing ID number."}), 400
    if not is_allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed."}), 400

    # Prepare file path
    try:
        extension = file.filename.rsplit(".", 1)[1].lower()
        file_path = f"students/{id_number}.{extension}"
        file_content = file.read()

        if len(file_content) == 0:
            return jsonify({"success": False, "message": "File is empty."}), 400

        supabase.storage.from_(STORAGE_BUCKET).upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": file.mimetype}
        )

        public_url = supabase.storage.from_(STORAGE_BUCKET).get_public_url(file_path).get("publicUrl")

        return jsonify({"success": True, "message": "File uploaded successfully.", "new_url": public_url})

    except Exception as e:
        print("Supabase Upload ERROR:", e)
        return jsonify({"success": False, "message": f"Upload failed: {e}"}), 500
    
@student_bp.route("/delete", methods=["POST"])
def delete_student():
    id_number = request.form.get("id_number")
    try:
        student_models.delete(id_number)
        flash("Student deleted successfully!", "success")
    except ValueError:
        flash("Student does not exist.", "danger")
    return redirect(url_for("student.students"))
