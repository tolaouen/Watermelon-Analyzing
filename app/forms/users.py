import re 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.users import User
from extensions import db


# set strong password 
def strong_password(form, field):
    """Custom validator to check for strong passwords."""
    password = field.data
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        raise ValidationError(
            'Password must be at least 8 characters long and include an uppercase letter, ''a lowercase letter, a number, and a special character.'
            )

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Enter username"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter email"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Enter password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
        render_kw={"placeholder": "Confirm password"},
    )

    submit = SubmitField("Save")

    def validate_username(self, username):
        existing_user = db.session.scalar(db.select(User).filter_by(username=username.data))
        if existing_user:
            raise ValidationError("Username already exists. Please choose a different username.")

    def validate_email(self, email):
        existing_email = db.session.scalar(db.select(User).filter_by(email=email.data))
        if existing_email:
            raise ValidationError("Email already registered. Please choose a different email.")

class UserUpdateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"autocomplete": "off"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"autocomplete": "off"},
    )

    submit = SubmitField("Update")

    def __init__(self, original_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, username):
        if username.data != self.original_user.username:
            existing_user = db.session.scalar(db.select(User).filter_by(username=username.data))
            if existing_user:
                raise ValidationError("Username already exists. Please choose a different username.")

    def validate_email(self, email):
        if email.data != self.original_user.email:
            existing_email = db.session.scalar(db.select(User).filter_by(email=email.data))
            if existing_email:
                raise ValidationError("Email already registered. Please choose a different email.")

class UserDeleteForm(FlaskForm):
    submit = SubmitField("Delete")
