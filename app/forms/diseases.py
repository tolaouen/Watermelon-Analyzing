from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.diseases import Disease

# Diagnosis Select form
class DiagnosisForm(FlaskForm):
    # These are populated dynamically in the view from the
    # available symptom names.
    symptom1 = SelectField(
        "Symptom 1",
        validators=[DataRequired()],
        render_kw={"placeholder": "Select First Symptom"},
        choices=[],
    )

    symptom2 = SelectField(
        "Symptom 2",
        validators=[DataRequired()],
        render_kw={"placeholder": "Select Second Symptom"},
        choices=[],
    )

    symptom3 = SelectField(
        "Symptom 3",
        validators=[DataRequired()],
        render_kw={"placeholder": "Select Third Symptom"},
        choices=[],
    )

    submit = SubmitField("Analyzing")
 
 
# Create Disease form
class CreateDiseaseForm(FlaskForm):
    name = StringField(
        "Disease Name",
        validators=[DataRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "Disease name"},
    )

    symptoms = TextAreaField(
        "Symptoms",
        validators=[DataRequired()],
        render_kw={"placeholder": "symptoms"},
    )

    causes = TextAreaField(
        "Causes",
        validators=[DataRequired()],
        render_kw={"placeholder": "causes"},
    )

    treatments = TextAreaField(
        "Treatments",
        validators=[DataRequired()],
        render_kw={"placeholder": "treatments"},
    )

    prevention = TextAreaField(
        "Prevention",
        validators=[DataRequired()],
        render_kw={"placeholder": "prevention methods"},
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
