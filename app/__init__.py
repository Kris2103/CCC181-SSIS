from flask import Flask, redirect, url_for
from app.database import close_db
from app.route.student.controller import student_bp
from app.route.dashboard.controller import dashboard_bp
from app.route.program.controller import program_bp
from app.route.college.controller import college_bp
from app.route.authentication.auth_controller import auth_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object("config")

    # Register all blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(student_bp, url_prefix="/students")
    app.register_blueprint(program_bp, url_prefix="/programs")
    app.register_blueprint(college_bp, url_prefix="/colleges")

    app.teardown_appcontext(close_db)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
