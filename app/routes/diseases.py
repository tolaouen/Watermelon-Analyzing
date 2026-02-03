from app.forms.diseases import CreateDiseaseForm, DeleteDiseaseForm, UpdateDiseaseForm, DiagnosisForm
from app.services.diseases import DiseaseService
from app.decorators import permission_required
from flask import Blueprint, flash, abort, render_template, redirect, url_for
from flask_login import login_required


disease_route = Blueprint("disease", __name__, url_prefix="/disease")

@disease_route.route("/", methods=["GET", "POST"])
@disease_route.route("/diagnose", methods=["GET", "POST"])
@login_required
@permission_required('diseases:read')
def index():
    form = DiagnosisForm()
    all_symptoms = DiseaseService.get_all_symptoms()

    # Populate select field choices with available symptom names
    choices = [("", "Select a symptom")] + [(s, s) for s in all_symptoms]
    form.symptom1.choices = choices
    form.symptom2.choices = choices
    form.symptom3.choices = choices

    if form.validate_on_submit():
        user_symptoms = [
            s.strip()
            for s in [
                form.symptom1.data,
                form.symptom2.data,
                form.symptom3.data,
            ]
            if s and s.strip()
        ]
        results = DiseaseService.diagnose_disease(user_symptoms)
        return render_template(
            "dashboard/result.html",
            results=results,
            symptoms=user_symptoms,
        )

    return render_template("dashboard/diagnose.html", form=form, symptoms=all_symptoms)


@disease_route.route("/create", methods=["GET", "POST"])
@login_required
@permission_required('diseases:manage')
def create():
    form = CreateDiseaseForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "symptoms": form.symptoms.data,
            "causes": form.causes.data,
            "treatments": form.treatments.data,
            "prevention": form.prevention.data
        }
        disease = DiseaseService.create_disease(data)
        flash(f"Disease {disease.name} was created successfully", "success")
        return redirect(url_for("disease.detail", disease_id=disease.id))
    return render_template("dashboard/create.html", form=form)

@disease_route.route("/<int:disease_id>")
@login_required
@permission_required('diseases:read')
def detail(disease_id: int):
    disease = DiseaseService.get_disease_by_id(disease_id)
    if disease is None:
        abort(404, "Disease Not Found")

    return render_template("dashboard/detail.html", disease=disease)
