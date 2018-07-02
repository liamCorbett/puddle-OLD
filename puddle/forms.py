from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from puddle.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=255)])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountInfoForm(FlaskForm):
    username = StringField('Username', validators=[Optional(), Length(min=4, max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose another one.')


class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body')
    submit = SubmitField('Post')