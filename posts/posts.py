from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from application import User, Job, db, Drafts
from forms import LoginForm, SignupForm, PasswordForm, NewJobForm
from flask_login import current_user, login_required

posts_bp = Blueprint('posts_bp', __name__,
                     template_folder='templates',
                     static_folder='static', static_url_path='assets')


@posts_bp.route('/edit-<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id):
    form = NewJobForm()
    post = Job.query.get_or_404(id)
    id = current_user.id

    if id == post.poster.id:
        if form.validate_on_submit():
            post.job_title = form.job_title.data
            post.state = form.state.data
            post.area = form.area.data
            post.suburb = form.suburb.data
            post.description = form.description.data
            post.highlight_1 = form.highlight_1.data
            post.highlight_2 = form.highlight_2.data
            post.highlight_3 = form.highlight_3.data
            post.deleted = "0"

            db.session.add(post)
            db.session.commit()
            flash("Post updated successfully", category='success')
            return render_template('edit_post.html', form=form, post=post)
        form.job_title.data = post.job_title
        form.state.data = post.state
        form.area.data = post.area
        form.suburb.data = post.suburb
        form.description.data = post.description
        form.highlight_1.data = post.highlight_1
        form.highlight_2.data = post.highlight_2
        form.highlight_3.data = post.highlight_3

        return render_template('edit_post.html', form=form, post=post)
    else:
        flash("Not authorised to edit post", category='success')
        return render_template('posts.html', form=form, post=post)


@posts_bp.route('/edit-draft-<int:id>', methods=["GET", "POST"])
@login_required
def edit_draft(id):
    form = NewJobForm()
    post = Drafts.query.get_or_404(id)
    id = current_user.id

    if id == post.poster.id:
        if form.validate_on_submit():
            post.job_title = form.job_title.data
            post.state = form.state.data
            post.area = form.area.data
            post.suburb = form.suburb.data
            post.description = form.description.data
            post.highlight_1 = form.highlight_1.data
            post.highlight_2 = form.highlight_2.data
            post.highlight_3 = form.highlight_3.data
            post.deleted = "0"

            db.session.add(post)
            db.session.commit()
            flash("Post updated successfully", category='success')
            return render_template('edit_post.html', form=form, post=post)
        form.job_title.data = post.job_title
        form.state.data = post.state
        form.area.data = post.area
        form.suburb.data = post.suburb
        form.description.data = post.description
        form.highlight_1.data = post.highlight_1
        form.highlight_2.data = post.highlight_2
        form.highlight_3.data = post.highlight_3

        return render_template('edit_post.html', form=form, post=post)
    else:
        flash("Not authorised to edit post", category='success')
        return render_template('posts.html', form=form, post=post)


@posts_bp.route('/delete-post/<int:id>', methods=["GET", "POST"])
@login_required
def delete_post(id):
    post_to_delete = Job.query.get_or_404(id)
    id = current_user.id

    if id == post_to_delete.poster.id:
        try:
            post_to_delete.deleted = True
            db.session.add(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully", category="warning")
            posts = Job.query.order_by(Job.date_posted)
            return redirect(url_for('posts_bp.active_listings', posts=posts))

        except:
            flash("Whoops, there's an error ")
            posts = Job.query.order_by(Job.date_posted)
            return render_template('add_job.html', posts=posts)
    else:
        flash("You aren't authorised to deleted this", category="warning")
        posts = Job.query.order_by(Job.date_posted)
        return render_template('posts.html', posts=posts)


@posts_bp.route('/obliterate/<int:id>', methods=["GET", "POST"])
@login_required
def obliterate_post(id):
    post_to_delete = Job.query.get_or_404(id)
    id = current_user.id

    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post obliterated successfully", category="warning")
            posts = Job.query.order_by(Job.date_posted)
            return redirect(url_for('posts_bp.active_listings', posts=posts))

        except:
            flash("Whoops, there's an error ")
            posts = Job.query.order_by(Job.date_posted)
            return render_template('dashboard.html', posts=posts)
    else:
        flash("You aren't authorised to deleted this", category="warning")
        posts = Job.query.order_by(Job.date_posted)
        return render_template('posts.html', posts=posts)


@posts_bp.route('/obliterate-draft/<int:id>', methods=["GET", "POST"])
@login_required
def obliterate_draft_post(id):
    draft_to_delete = Drafts.query.get_or_404(id)
    id = current_user.id

    if id == draft_to_delete.poster.id:
        try:
            db.session.delete(draft_to_delete)
            db.session.commit()
            flash("Post obliterated successfully", category="warning")
            posts = Drafts.query.order_by(Drafts.date_posted)
            return redirect(url_for('posts_bp.draft', posts=posts))

        except:
            flash("Whoops, there's an error ")
            posts = Drafts.query.order_by(Drafts.date_posted)
            return render_template('drafts.html', posts=posts)
    else:
        flash("You aren't authorised to deleted this", category="warning")
        posts = Drafts.query.order_by(Drafts.date_posted)
        return render_template('dashboard.html', posts=posts)


@posts_bp.route('/restore-post/<int:id>', methods=["GET", "POST"])
@login_required
def restore_post(id):
    post_to_restore = Job.query.get_or_404(id)
    id = current_user.id

    if id == post_to_restore.poster.id:
        try:
            post_to_restore.deleted = False
            db.session.add(post_to_restore)
            db.session.commit()
            flash("Post restored successfully", category="success")
            posts = Job.query.order_by(Job.date_posted)
            return redirect(url_for('posts_bp.active_listings', posts=posts))

        except:
            flash("Whoops, there's an error ")
            posts = Job.query.order_by(Job.date_posted)
            return render_template('index.html', posts=posts)
    else:
        flash("You aren't authorised to delete this", category="warning")
        posts = Job.query.order_by(Job.date_posted)
        return render_template('index.html', posts=posts)


# TODO: Add a preview component to display on the right of the 'add-job' form
@posts_bp.route('/add-job', methods=["GET", "POST"])
@login_required
def add_job():
    form = NewJobForm()
    posts = Job.query.order_by(Job.date_posted.desc())
    if form.validate_on_submit():
        poster = current_user.id
        job = Job(job_title=form.job_title.data, state=form.state.data, area=form.area.data, suburb=form.suburb.data,
                  description=form.description.data,
                  highlight_1=form.highlight_1.data, highlight_2=form.highlight_2.data,
                  highlight_3=form.highlight_3.data, poster_id=poster, deleted=0)
        form.job_title.data = ''
        form.state.data = ''
        form.area.data = ''
        form.suburb.data = ''

        form.description.data = ''

        form.highlight_1.data = ''
        form.highlight_2.data = ''
        form.highlight_3.data = ''
        db.session.add(job)
        db.session.commit()
        flash("Job post submitted successfully", category='success')
    return render_template('add_job.html', form=form, post=posts)


@posts_bp.route('/posts', methods=["GET"])
def posts():
    posts = Job.query.order_by(Job.date_posted.desc())
    return render_template('posts.html', posts=posts)


@posts_bp.route('/posts/<int:id>', methods=["GET"])
def display_post(id):
    post = Job.query.get_or_404(id)
    id = post.id
    return render_template('large-post.html', id=id, post=post)


@posts_bp.route('/active-listings', methods=["GET", "POST"])
@login_required
def active_listings():
    posts = Job.query.order_by(Job.date_posted.desc())
    return render_template('user_active_listings.html', posts=posts)


@posts_bp.route('/deleted-listings', methods=["GET"])
@login_required
def deleted_listings():
    posts = Job.query.order_by(Job.date_posted)
    return render_template('user_deleted_listings.html', posts=posts)


@posts_bp.route('/drafts', methods=["GET", "POST"])
@login_required
def draft():
    form = NewJobForm()
    posts = Drafts.query.order_by(Drafts.id.desc())

    # if form.validate_on_submit():
    if request.method == "POST":
        poster = current_user.id
        draft = Drafts(job_title=form.job_title.data, state=form.state.data, area=form.area.data,
                       suburb=form.suburb.data,
                       description=form.description.data,
                       highlight_1=form.highlight_1.data, highlight_2=form.highlight_2.data,
                       highlight_3=form.highlight_3.data, poster_id=poster, deleted=0)
        form.job_title.data = ''
        form.state.data = ''
        form.area.data = ''
        form.suburb.data = ''
        form.description.data = ''
        form.highlight_1.data = ''
        form.highlight_2.data = ''
        form.highlight_3.data = ''
        db.session.add(draft)
        db.session.commit()
        flash("Saved to drafts", category='success')
    else:
        return render_template('drafts.html', form=form, posts=posts)
    return render_template('drafts.html', form=form, posts=posts)


@posts_bp.route('/preview-<int:id>', methods=["POST", "GET"])
@login_required
def preview(id):
    post = Drafts.query.get_or_404(id)
    id = current_user.id
    if id == post.poster.id:
        return render_template('preview.html', post=post)
    return render_template('dashboard.html', post=post)

@posts_bp.route('/draft-to-post-<int:id>', methods=["POST", "GET"])
def draft_to_post(id):
    draft = Drafts.query.get_or_404(id)
    poster = current_user.id

    job = Job(job_title=draft.job_title, state=draft.state, area=draft.area, suburb=draft.suburb,
              description=draft.description,
              highlight_1=draft.highlight_1, highlight_2=draft.highlight_2,
              highlight_3=draft.highlight_3, poster_id=poster, deleted=0)
    db.session.add(job)
    db.session.delete(draft)
    db.session.commit()
    flash("Job post submitted successfully", category='success')
    posts = Job.query.order_by(Job.date_posted.desc())
    return redirect(url_for('posts_bp.active_listings', posts=posts))
