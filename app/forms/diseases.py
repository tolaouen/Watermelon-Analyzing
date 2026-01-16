from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.diseases import Disease

# Create Disease form
class CreateDiseaseForm(FlaskForm):
    name = StringField(
        "Disease Name",
        validators=[DataRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "Enter disease name"},
    )

    symptoms = TextAreaField(
        "Symptoms",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter symptoms"},
    )

    causes = TextAreaField(
        "Causes",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter causes"},
    )

    treatments = TextAreaField(
        "Treatments",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter treatments"},
    )

    prevention = TextAreaField(
        "Prevention",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter prevention methods"},
    )

    submit = SubmitField("Save")

    def validate_name(self, name):
        exists_disease = db.session.scalar(db.select(Disease).filter_by(name=name.data))
        if exists_disease:
            raise ValidationError("This is already exist.")

# Update Disease form
class UpdateDiseaseForm(FlaskForm):
    name = StringField(
        "Disease Name",
        validators=[DataRequired(), Length(min=3, max=100)],
    )

    symptoms = TextAreaField(
        "Symptoms",
        validators=[DataRequired()],
    )

    causes = TextAreaField(
        "Causes",
        validators=[DataRequired()],
    )

    treatments = TextAreaField(
        "Treatments",
        validators=[DataRequired()],
    )

    prevention = TextAreaField(
        "Prevention",
        validators=[DataRequired()],
    )

    submit = SubmitField("Update")

    def __init__(self, original_disease, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_disease = original_disease

    def validate_name(self, name):
        if name.data != self.original_disease.name:
            exists_disease = db.session.scalar(db.select(Disease).filter_by(name=name.data))

            if exists_disease:
                raise ValidationError("This name is already exist.")

# Delete Disease form
class DeleteDiseaseForm(FlaskForm):
    submit = SubmitField("Delete")