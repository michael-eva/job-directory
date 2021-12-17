from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from forms import LoginForm, SignupForm, PasswordForm, NewJobForm
from wtforms.validators import Email
from application import User, Job, db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # checking to see if user has been deleted
            if user.deleted == "1":
                flash("No user found, please check details or sign up", category='warning')
                return redirect(url_for('auth_bp.login'))
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('dashboard_bp.dashboard'))
            else:
                flash("Wrong password, try again", category='warning ')
        else:
            flash("No user found, please check details or sign up", category='warning')
    return render_template('login.html', form=form)


@auth_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category='warning')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Account exists, please log in', category='warning')
        if user is None:
            user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data,
                        company=form.company.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

            form.firstname.data = ''
            form.lastname.data = ''
            form.company.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            form.confirm.data = ''
            flash('Account created', category='success')
    users = User.query.order_by(User.date_added)
    return render_template('signup.html', form=form, users=users)


# TODO: validate email address if email address is updated
@auth_bp.route('/update-<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
    form = SignupForm()
    name_to_update = User.query.get_or_404(id)
    id = current_user.id
    if id == name_to_update.id or id == 1:
        if request.method == "POST":
            name_to_update.firstname = form.firstname.data
            name_to_update.lastname = form.lastname.data
            name_to_update.company = form.company.data
            name_to_update.email = form.email.data
            # TODO: validate email address
            try:
                db.session.commit()
                flash("User updated successfully", category='success')
                return redirect(url_for('dashboard_bp.dashboard', form=form, name_to_update=name_to_update))
            except:
                flash("Whoops, there's an error ")
                return render_template('update_user.html', form=form, name_to_update=name_to_update)
        else:
            return render_template('update_user.html', form=form, name_to_update=name_to_update)
    else:
        flash("You aren't allowed to be here", category='warning')
        # TODO: create a 404 page
        return redirect(url_for('404'))


# TODO: Delete all posts from user when user is deleted
@auth_bp.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        # making the user inactive rather than deleting from the database
        user_to_delete.deleted = True
        logout_user()
        db.session.add(user_to_delete)
        db.session.commit()

        flash("User deleted successfully", category="warning")
        users = User.query.order_by(User.date_added)
        return render_template('users.html', users=users)

    except:
        flash("Whoops, there's an error ")
        users = User.query.order_by(User.date_added)
        return render_template('signup.html', users=users)


@auth_bp.route('/restore/<int:id>', methods=["GET", "POST"])
def restore(id):
    user_to_restore = User.query.get_or_404(id)
    try:
        # making the user inactive rather than deleting from the database
        user_to_restore.deleted = False
        db.session.add(user_to_restore)
        db.session.commit()

        flash("User restored successfully", category="warning")
        users = User.query.order_by(User.date_added)
        return render_template('users.html', users=users)

    except:
        flash("Whoops, there's an error ")
        users = User.query.order_by(User.date_added)
        return render_template('index.html', users=users)
