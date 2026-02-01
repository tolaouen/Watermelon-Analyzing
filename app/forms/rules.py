from app.models.rules import Rules
from extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField   
from wtforms.validators import DataRequired, Length, ValidationError


class RulesForm(FlaskForm):
    name_1 = StringField(
        "Rule Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Rule Name 1"},
    
    )
    name_2 = StringField(
        "Rule Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Rule Name 2"},
    
    )
    name_3 = StringField(
        "Rule Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Rule Name 3"},
    
    )

    submit = StringField("Save")


class CreateRuleForm(FlaskForm):
    name = StringField(
        "Rule Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Rule Name"},
    )

    condition = BooleanField(
        "Condition",
        render_kw={"placeholder": "Condition"},
    )

    answer = TextAreaField(
        "Answer",
        validators=[DataRequired()],
        render_kw={"placeholder": "Answer"},
    )

    submit = SubmitField("Save")

class UpdateRuleForm(FlaskForm):
    name = StringField(
        "Rule Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Rule Name"}, 
    )

    condition = BooleanField("Condition", default=False)

    answer = TextAreaField(
        "Answer",
        validators=[DataRequired()],
        render_kw={"placeholder": "Answer"},
    )

    submit = SubmitField("Update")


class DeleteRuleForm(FlaskForm):
    submit = SubmitField("Delete")


        