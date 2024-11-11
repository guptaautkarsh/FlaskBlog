from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                    [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                    [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm_Password',
                        [DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username): #custom validator
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose an other one')

    def validate_email(self, email): #custom validator
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose an other one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                    [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                    [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                    [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username): #custom validator
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose an other one')

    def validate_email(self, email): #custom validator
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose an other one')


class PostForm(FlaskForm):
    title = StringField('Title',
                    [DataRequired()])
    content = TextAreaField('Content',
                    [DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email): #custom validator
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm_Password',
                                     [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')