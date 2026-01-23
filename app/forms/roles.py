
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from extensions import db
from app.models.roles import Role
from app.models.permissions import Permission

class CreateRoleForm(FlaskForm):
    name = StringField(
        "Role Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Role Name"},
    )

    description = StringField(
        "Description",
        render_kw={"placeholder": "Description"},
    )

    permissions = SelectField(
        "Permissions",
        coerce=int,
        validators=[Optional()],
        render_kw={"placeholder": "Permissions"},
    )

    submit = SubmitField("Save")

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

    description = StringField("Description")

    permissions = SelectField(
        "Permissions",
        coerce=int,
    )

    submit = SubmitField("Update")

    def __init__(self, original_role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_role = original_role
        self.permissions.choices = [(0, "Select Permission")] + [(p.id, f"{p.code} - {p.name}") for p in Permission.query.order_by(Permission.name).all()]
        # Set initial form data
        self.name.data = original_role.name
        self.description.data = original_role.description
        if original_role.permissions:
            self.permissions.data = original_role.permissions[0].id
        else:
            self.permissions.data = 0

    def validate_name(self, name):
        if name.data != self.original_role.name:
            existing_role = db.session.scalar(db.select(Role).filter_by(name=name.data))

            if existing_role:
                raise ValidationError("Role name already exists. Please choose a different name.")

class DeleteRoleForm(FlaskForm):
    submit = SubmitField("Delete Role")
