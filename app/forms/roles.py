
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
        render_kw={"placeholder": "Role Name"},
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "Description"},
    )

    permissions = SelectMultipleField(
        "Permissions",
        coerce=int,
        render_kw={"size": 10},
    )

    submit = SubmitField("Create Role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions.choices = [(p.id, f"{p.code} - {p.name}") for p in Permission.query.order_by(Permission.name).all()]

    def validate_name(self, name):
        existing_role = db.session.scalar(db.select(Role).filter_by(name=name.data))
        if existing_role:
            raise ValidationError("Role name already exists. Please choose a different name.")

class UpdateRoleForm(FlaskForm):
    name = StringField(
        "Role Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Role Name"},
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "Description"}
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
        self.permissions.choices = [(p.id, f"{p.code} - {p.name}") for p in Permission.query.order_by(Permission.name).all()]
        # Set initial form data
        self.name.data = original_role.name
        self.description.data = original_role.description
        self.permissions.data = [p.id for p in original_role.permissions]

    def validate_name(self, name):
        if name.data != self.original_role.name:
            existing_role = db.session.scalar(db.select(Role).filter_by(name=name.data))

            if existing_role:
                raise ValidationError("Role name already exists. Please choose a different name.")

class DeleteRoleForm(FlaskForm):
    submit = SubmitField("Delete Role")
