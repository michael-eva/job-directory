import email_validator
from flask import Flask, render_template, flash, get_flashed_messages, request, url_for, redirect, jsonify, session
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from forms import LoginForm, SignupForm, PasswordForm, NewJobForm, FilterForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime
import config


application = Flask(__name__)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
application.config.from_object("config.DevelopmentConfig")


def create_app():
    db.init_app(application)

    from auth.auth import auth_bp
    from posts.posts import posts_bp
    from user.user import user_bp
    from dashboard.dashboard import dashboard_bp
    from admin.admin import admin_bp

    application.register_blueprint(auth_bp, url_prefix='')
    application.register_blueprint(posts_bp, url_prefix='')
    application.register_blueprint(user_bp, url_prefix='')
    application.register_blueprint(dashboard_bp, url_prefix='')
    application.register_blueprint(admin_bp, url_prefix='')

    return application


login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'auth_bp.login'
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200))
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # One to many relationship with 'Job' class
    jobs = db.relationship('Job', backref='poster')
    drafts = db.relationship('Drafts', backref='poster')

    # Archiving deleted user accounts
    deleted = db.Column(db.String(5), default=0)

    @property
    def password(self):
        raise AttributeError('not valid')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255))
    state = db.Column(db.String(255))
    area = db.Column(db.String(255))
    suburb = db.Column(db.String(255))
    description = db.Column(db.Text)
    highlight_1 = db.Column(db.Text)
    highlight_2 = db.Column(db.Text)
    highlight_3 = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.String(5))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Drafts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255))
    state = db.Column(db.String(255))
    area = db.Column(db.String(255))
    suburb = db.Column(db.String(255))
    description = db.Column(db.Text)
    highlight_1 = db.Column(db.Text)
    highlight_2 = db.Column(db.Text)
    highlight_3 = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.String(5))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    state = db.relationship('Area', backref='get_area')


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))


@application.route('/')
def index():
    form = FilterForm()
    posts = Job.query.all()
    form.state.choices = [(state.id, state.name) for state in State.query.all()]
    if request.method == 'POST':
        area = Area.query.filter_by()
        return '<h1>State: {}, Area: {}</h1>'.format(form.state.data, area.name)
    return render_template('index.html', form=form, posts=posts)


@application.route('/area/<get_area>')
def areabystate():
    areas = Area.query.filter_by(state_id=get_area).all()
    areaArray = []
    for area in areas:
        areaObj = {}
        areaObj['id'] = area.id
        areaObj['name'] = area.name
        areaArray.append(areaObj)
    return jsonify({'statearea': areaArray})


#
# def filter_search():
#     form = FilterForm()
#     state = form.state.data
#     area = ''
#     if state == "WA":
#         form.area.choices = [('perth, Perth'), ('peel, Peel')]
#         return render_template('index.html', posts=posts, state=state, area=area, form=form)


if __name__ == '__main__':
    napp = create_app()
    napp.run()
