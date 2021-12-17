import email_validator
from flask import Flask, render_template, flash, get_flashed_messages, request, url_for, redirect, jsonify, session, Blueprint
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from forms import LoginForm, SignupForm, PasswordForm, NewJobForm, FilterForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


admin_bp = Blueprint('admin_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')


@admin_bp.route('/admin', methods=["GET"])
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html')
    else:
        flash('Sorry, only admin can access this page', category='warning')
        return redirect(url_for('dashboard_bp.dashboard'))