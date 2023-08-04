from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user
from app.services import save_course_to_profile, get_favorite_courses, remove_course_from_profile, remove_all_courses_from_profile

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/save', methods=['GET'])
def save():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))

    course_name = request.args.get('course_name')
    course_url = request.args.get('course_url')

    existing_courses = [c.course_name for c in get_favorite_courses(current_user.id)]

    if course_name and course_url:
        if course_name in existing_courses:
            flash('Course already saved')
            return redirect(url_for('user.favs'))

        course = {'name': course_name, 'url': course_url}
        success = save_course_to_profile(current_user.id, course)
        if success:
            flash('Course saved successfully', 'success')
        else:
            flash('Failed to save course', 'danger')
        return redirect(url_for('user.favs'))
    else:
        flash('Course not found', 'danger')
        return redirect(url_for('home.index'))


@user_bp.route('/favs', methods=['GET'])
def favs():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))
    
    courses = get_favorite_courses(current_user.id)
    return render_template('favs.html', courses=courses)


@user_bp.route('/remove', methods=['GET'])
def remove():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))
    
    course_name = request.args.get('course_name')
    if course_name:
        success = remove_course_from_profile(current_user.id, course_name)
        if success:
            flash('Course removed successfully', 'success')
        else:
            flash('Failed to remove course', 'danger')

    return redirect(url_for('user.favs'))


@user_bp.route('/remove_all', methods=['GET'])
def remove_all():
    if not current_user.is_authenticated:
        flash('User not logged in', 'danger')
        return redirect(url_for('auth.login'))
    
    courses = get_favorite_courses(current_user.id)
    if not courses:
        flash('No courses to remove', 'warning')
        return redirect(url_for('user.favs'))
    
    success = remove_all_courses_from_profile(current_user.id)
    if success:
        flash('All courses removed successfully', 'success')
    else:
        flash('Failed to remove courses', 'danger')

    return redirect(url_for('user.favs'))