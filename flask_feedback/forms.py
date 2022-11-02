from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_feedback.models import Users


class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=20)])

    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8, max=50)])

    email = StringField('Email',
        validators=[DataRequired(), Email(), Length(max=50)])

    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=30)])

    last_name = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=30)])

    submit = SubmitField('Create Account')



class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=20)])

    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8, max=50)])

    submit = SubmitField('Login')


class FeedbackForm(FlaskForm):
    title = StringField('Title',
        validators=[DataRequired(), Length(min=1, max=100)])

    content = TextAreaField('Body',
        validators=[DataRequired(), Length(min=1, max=250)])

    submit = SubmitField('Save')