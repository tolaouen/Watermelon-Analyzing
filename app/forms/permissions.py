from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.permissions import Permission

class CreatePermissionForm(FlaskForm):
    name = StringField(
        "Permission Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Enter permission name"},
    )
    code = StringField(
        "Permission Code",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Enter permission code"},
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "Enter permission description"},
    )

    submit = SubmitField("Create Permission")

    def validate_name(self, name):
        existing_permission = db.session.scalar(db.select(Permission).filter_by(name=name.data))
        if existing_permission:
            raise ValidationError("Permission name already exists. Please choose a different name.")

    def validate_code(self, code):
        existing_permission = db.session.scalar(db.select(Permission).filter_by(code=code.data))
        if existing_permission:
            raise ValidationError("Permission code already exists. Please choose a different code.")
        
class UpdatePermissionForm(FlaskForm):
    name = StringField(
        "Permission Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"autocomplete": "off"},
    )
    code = StringField(
        "Code",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"autocomplete": "off"},
    )
    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
    )

    submit = SubmitField("Update Permission")

    def __init__(self, original_permission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_permission = original_permission
        # Set initial form data
        self.name.data = original_permission.name
        self.code.data = original_permission.code
        self.description.data = original_permission.description

    def validate_name(self, name):
        if name.data != self.original_permission.name:
            existing_permission = db.session.scalar(db.select(Permission).filter_by(name=name.data))

            if existing_permission:
                raise ValidationError("Permission name already exists. Please choose a different name.")

    def validate_code(self, code):
        if code.data != self.original_permission.code:
            existing_permission = db.session.scalar(db.select(Permission).filter_by(code=code.data))

            if existing_permission:
                raise ValidationError("Permission code already exists. Please choose a different code.")

class DeletePermissionForm(FlaskForm):
    submit = SubmitField("Delete Permission")
