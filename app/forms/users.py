import re 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models.users import User
from app.models.roles import Role
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
        render_kw={"placeholder": "Username"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )

    full_name = StringField(
        "Full Name",
        validators=[Optional(), Length(max=120)],
        render_kw={"placeholder": "Full Name"},
    )

    is_active = BooleanField("Is Active", default=True)

    role_id = SelectField(
        "Role",
        coerce=int,
        validators=[Optional()],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
        render_kw={"placeholder": "Confirm Password"},
    )

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = [(0, "Select Role")] + [
            (role.id, role.name) for role in Role.query.order_by(Role.name).all()
        ]

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
        render_kw={"placeholder": "Username"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )

    full_name = StringField(
        "Full Name",
        validators=[Optional(), Length(max=120)],
        render_kw={"placeholder": "Full Name"},
    )

    is_active = BooleanField("Is Active", default=True)

    role_id = SelectField(
        "Role",
        coerce=int,
        validators=[Optional()],
        render_kw={"placeholder": "Role"},
    )

    password = PasswordField(
        "Password",
        validators=[Optional()],
        render_kw={"placeholder": "Password"},
    )

    confirm_password = PasswordField (
        "Confirm_Password",
        validators=[Optional()],
        render_kw={"placeholder": "Confirm Password"}
    )
    submit = SubmitField("Update")

    def __init__(self, original_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user
        self.role_id.choices = [(0, "Select Role")] + [
            (role.id, role.name) for role in Role.query.order_by(Role.name).all()
        ]

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
