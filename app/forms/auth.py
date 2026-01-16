from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo

# Set strong password 
def strong_password(form, field):
    password = field.data
    if (len(password) < 8 or
        not any(c.islower() for c in password) or
        not any(c.isupper() for c in password) or
        not any(c.isdigit() for c in password) or
        not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password)):
        raise ValidationError(
            'Password must be at least 8 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character.'
            )
#  Login form of authentication   
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter username"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )

    remember_me = BooleanField("Remember Me", default=False)

    submit = SubmitField("Login")

#  Register form of authentication
class RegisterForm(FlaskForm):
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

    submit = SubmitField("Register")