from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.permissions import Permission
from app.models.modules import Module

class CreatePermissionForm(FlaskForm):
    name = StringField(
        "Permission Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Name"},
    )
    code = StringField(
        "Permission Code",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Code"},
    )
    module = SelectField(
        "Module",
        validators=[DataRequired()],
        coerce=int
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "Description"},
    )

    submit = SubmitField("Add Permission")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module.choices = [(m.id, m.name) for m in Module.query.order_by(Module.name).all()]

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
        render_kw={"placeholder": "Name"},
    )
    code = StringField(
        "Code",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Code"},
    )
    module = SelectField(
        "Module",
        validators=[DataRequired()],
        coerce=int
    )

    description = TextAreaField("Description")

    submit = SubmitField("Update Permission")

    def __init__(self, original_permission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_permission = original_permission
        self.module.choices = [(m.id, m.name) for m in Module.query.order_by(Module.name).all()]
        # Set initial form data
        self.name.data = original_permission.name
        self.code.data = original_permission.code
        self.description.data = original_permission.description
        # Assuming single module, get first or something, but for now, if it has modules, set to first
        if original_permission.modules:
            self.module.data = original_permission.modules[0].id

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
    submit = SubmitField("Delete")
