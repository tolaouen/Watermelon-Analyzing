from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.modules import Module

class MuduleForm(FlaskForm):
    name = StringField(
        "Module Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "eg. Knowledge Base", "autocomplete": "off"},
        filters=[lambda x: x.strip() if isinstance(x, str) else x],
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        render_kw={"placeholder": "What is module use for? (optional)"},
        filters=[lambda x: x.strip() if isinstance(x, str) else x],
    )

    submit = SubmitField("Create")

    def validate_name(self, name):
        existing_module = db.sessoin.scalar(db.select(Module).filter_by(name=name.data))
        if existing_module:
            raise ValidationError("Module name already exists. Please choose a different name.")
        
class UpdateModuleForm(FlaskForm):
    name = StringField(
        "Module Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"autocomplete": "off"},
        filters=[lambda x: x.strip() if isinstance(x, str) else x],
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=200)],
        filters=[lambda x: x.strip() if isinstance(x, str) else x],
    )

    submit = SubmitField("Update")

    def __init__(self, original_module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_module = original_module

    def validate_name(self, name):
        if name.data != self.original_module.name:
            existing_module = db.sessoin.scalar(db.select(Module).filter_by(name=name.data))

            if existing_module:
                raise ValidationError("Module name already exists. Please choose a different name.")
            
class DeleteModuleForm(FlaskForm):
    submit = SubmitField("Delete")
    