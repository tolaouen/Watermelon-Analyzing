from app.forms.diseases import CreateDiseaseForm, DeleteDiseaseForm, UpdateDiseaseForm
from app.services.diseases import DiseaseService
from flask import Blueprint, flash, abort, render_template, redirect, url_for
from flask_login import login_required


disease_route = Blueprint("disease", __name__, url_prefix="/disease")

@disease_route.route("/")
@login_required
def index():
    disease = DiseaseService.get_all_symptoms()
    return render_template("dashboard/diagnose.html", disease=disease)




