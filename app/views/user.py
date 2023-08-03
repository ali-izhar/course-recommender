from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user
from app.services import save_course_to_profile, get_favorite_courses

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/save', methods=['GET'])
def save():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))

    course_name = request.args.get('course_name')
    course_url = request.args.get('course_url')
    return_url = request.args.get('return_url', url_for('main.index'))
    
    if course_name and course_url:
        course = {'name': course_name, 'url': course_url}
        success = save_course_to_profile(current_user.id, course)
        if success:
            flash('Course saved successfully', 'success')
        else:
            flash('Failed to save course', 'danger')
        return redirect(return_url)
    else:
        flash('Course not found', 'warning')
        return redirect(return_url)


@user_bp.route('/favs', methods=['GET'])
def favs():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth_bp.login'))
    
    courses = get_favorite_courses(current_user.id)
    return render_template('favs.html', courses=courses)