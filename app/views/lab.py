from flask import Blueprint, render_template, session
from flask_login import current_user, login_required

lab_bp = Blueprint('lab', __name__, url_prefix='/lab')

@lab_bp.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')