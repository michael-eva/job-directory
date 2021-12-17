from flask import Blueprint, request, render_template, flash, redirect, url_for
from application import User
from flask_login import login_required, current_user

user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')


@user_bp.route('/users', methods=["GET"])
@login_required
def user_page():
    id = current_user.id
    if id == 1:
        users = User.query.order_by(User.date_added)
        return render_template('users.html', users=users)
    else:
        flash('Sorry, only admin can access this page', category='warning')
        return redirect(url_for('dashboard_bp.dashboard'))


@user_bp.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html')
