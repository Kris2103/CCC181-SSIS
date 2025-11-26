from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import user_models
from app.decorator.decorators import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation for @gmail.com addresses
        if not email.lower().endswith('@gmail.com'):
            flash('Only @gmail.com addresses are allowed for registration.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validation for unique username
        if user_models.get_by_username(username):
            flash('That username is already taken.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validation for unique email
        if user_models.get_by_email(email):
            flash('That email address is already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create the new user
        user_models.create(username, email, password)
        
        flash('Registration successful! Please log in with your email.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = user_models.get_by_email(email)
        
        # Check if user exists and password is correct
        if user and user_models.check_password(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            flash(f"Welcome back, {user['username']}!", 'success')
            
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))