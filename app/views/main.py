from flask import Blueprint, render_template, session
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
@login_required
def index():
    session.permanent = False
    return render_template('index.html', user=current_user)


@main_bp.route('/team')
def team():
    return render_template('team.html')