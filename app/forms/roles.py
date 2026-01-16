
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.roles import Role
from app.models.permissions import Permission

class CreateRoleForm(FlaskForm):
    name = StringField(
        "Role Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Enter role name"},
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "Enter role description (optional)"},
    )

    permissions = SelectMultipleField(
        "Permissions",
        coerce=int,
        render_kw={"size": 10},
    )

    submit = SubmitField("Create Role")

    def validate_name(self, name):
        existing_role = db.session.scalar(db.select(Role).filter_by(name=name.data))
        if existing_role:
            raise ValidationError("Role name already exists. Please choose a different name.")

class UpdateRoleForm(FlaskForm):
    name = StringField(
        "Role Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"autocomplete": "off"},
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
    )

    permissions = SelectMultipleField(
        "Permissions",
        coerce=int,
        render_kw={"size": 10},
    )

    submit = SubmitField("Update Role")

    def __init__(self, original_role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_role = original_role

    def validate_name(self, name):
        if name.data != self.original_role.name:
            existing_role = db.session.scalar(db.select(Role).filter_by(name=name.data))

            if existing_role:
                raise ValidationError("Role name already exists. Please choose a different name.")

class DeleteRoleForm(FlaskForm):
    submit = SubmitField("Delete Role")
