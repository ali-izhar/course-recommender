from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.services import create_user, get_user_by_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_user_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
            else:
                flash('Invalid password!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out. See you again soon!')
    return redirect(url_for('auth.login'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters!', category='error')
        else:
            user = get_user_by_email(email)
            if user:
                flash('Email already exists!', category='error')
            else:
                user = create_user(email, generate_password_hash(password1, method='sha256'))
                flash('Account created!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
    return render_template("signup.html", user=current_user)