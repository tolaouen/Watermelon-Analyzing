
from app.models.symptom import Symptoms
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from extensions import db
from app.models.diseases import Disease


class CreateSymptom(FlaskForm):

    name = StringField(
        "Symptom Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Symptom Name"}
    )

    description = TextAreaField(
        "Description",
        render_kw={"placeholder": "Description"},
    )

    submit = SubmitField("Save")

    def validate_name(self, name):
        existing_symptom = db.session.scalar(db.select(Symptoms).filter_by(name=name.data))
        if existing_symptom:
            raise ValidationError("Symptom name already exists. Please choose a different name.")

class UpdateSymptom(FlaskForm):

    name = StringField(
        "Symptom Name",
        render_kw=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Symptom Name"}
    )

    description = TextAreaField(
        "Description",
        render_kw={"placeholder": "Description"}, 
    )

    submit = SubmitField("Update")

    def __init__(self, original_symptom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_symptom = original_symptom
        self.name.data = original_symptom.name
        self.description.data = original_symptom.description    

    def validate(self, extra_validators = None):
        return super().validate(extra_validators)   
    

class DeleteSymptom(FlaskForm):
    submit = SubmitField("Delete")


        


    



