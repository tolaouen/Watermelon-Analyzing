from app.forms.diseases import CreateDiseaseForm, DeleteDiseaseForm, UpdateDiseaseForm, DiagnosisForm
from app.services.diseases import DiseaseService
from flask import Blueprint, flash, abort, render_template, redirect, url_for
from flask_login import login_required


disease_route = Blueprint("disease", __name__, url_prefix="/disease")

@disease_route.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = DiagnosisForm()
    symptoms = DiseaseService.get_all_symptoms()

    if form.validate_on_submit():
        user_symptoms = [s.strip() for s in form.symptoms.data.split(',')]
        results = DiseaseService.diagnose_disease(user_symptoms)
        return render_template("dashboard/result.html", results=results, symptoms=user_symptoms)

    return render_template("dashboard/diagnose.html", form=form, symptoms=symptoms)


@disease_route.route("/create", methods=["GET", "POST"])
@login_required
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
def detail(disease_id: int):
    disease = DiseaseService.get_disease_by_id(disease_id)
    if disease is None:
        abort(404, "Disease Not Found")

    return render_template("dashboard/detail.html", disease=disease)
