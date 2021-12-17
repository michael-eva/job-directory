from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField
from wtforms.validators import EqualTo, Email, InputRequired, Length
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password_hash = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    remember = BooleanField('Remember')
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(), Length(max=80)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(max=80)])
    email = StringField('Email', validators=[InputRequired(), Email(message="not a valid email address")])
    company = StringField('Company (not required)')
    password_hash = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128),
                                                          EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=128)])
    deleted = BooleanField('Deleted?')
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="not a valid email address")])
    password_hash = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    submit = SubmitField('Submit')


class NewJobForm(FlaskForm):
    job_title = StringField("Job Title", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])
    area = StringField("Area", validators=[InputRequired()])
    suburb = StringField("Suburb", validators=[InputRequired()])
    description = StringField("description", validators=[InputRequired()], widget=TextArea())
    highlight_1 = StringField("Enter 3 highlighted points:", validators=[InputRequired()])
    highlight_2 = StringField("Enter a higlighted point:")
    highlight_3 = StringField("Enter a higlighted point:")

    submit = SubmitField('Submit')
    draft = SubmitField('Save to drafts')
    preview = SubmitField('Preview')


class FilterForm(FlaskForm):
    state = SelectField('State',
                        choices=[])
# TODO: Filter this list based on the state selected
    area = SelectField('Area',
                       choices=[])

    submit = SubmitField('Filter')
