from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from application import Job, User, db
from forms import NewJobForm

dashboard_bp = Blueprint('dashboard_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')

@dashboard_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    posts = Job.query.order_by(Job.date_posted.desc())
    return render_template('dashboard.html', posts=posts)

@dashboard_bp.route('/dashboard/update/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
    form = SignupForm()
    name_to_update = User.query.get_or_404(id)
    if current_user.id == name_to_update.id:
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
        #TODO: create a 404 page
        return redirect(url_for('404'))



