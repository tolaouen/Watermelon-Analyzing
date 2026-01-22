from app.forms.roles import CreateRoleForm, UpdateRoleForm, DeleteRoleForm
from app.services.roles import RolesService
from flask import Blueprint, abort, render_template, redirect, flash, url_for
from flask_login import login_required
from extensions import db

role_router = Blueprint("Role", __name__, url_prefix="/role")

@role_router.route("/")
@login_required
def index():
    roles = RolesService.get_role_all()
    return render_template("roles/index.html", roles=roles)
@role_router.route("/<int:role_id>")
@login_required
def detail(role_id: int):
    role = RolesService.get_role_by_id(role_id)
    if role is None:
        abort(404, "Role Not Found")
    
    return render_template("roles/detail.html", role=role)

@role_router.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = CreateRoleForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        permission_id = [form.permissions.data] if form.permissions.data else []
        role = RolesService.create_role(data, permission_id)
        flash(f"Role {role.name} created successfully", "success")
        return redirect(url_for("Role.index"))
    return render_template("roles/create.html", form=form)

@role_router.route("/<int:role_id>/edit", methods=["GET", "POST"])
@login_required
def edit(role_id: int):
    roles = RolesService.get_role_by_id(role_id)

    if roles is None:
        abort(404, "Role Not Found")

    form = UpdateRoleForm(roles)
    
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        permission_id = [form.permissions.data] if form.permissions.data else []
        RolesService.update_role(roles, data, permission_id)
        flash(f"Role {roles.name} updated successfully", "success")
        return redirect(url_for("Role.detail", role_id=roles.id))
    return render_template("roles/edit.html", form=form, roles=roles)

@role_router.route("/<int:role_id>/delete", methods=["GET"])
@login_required
def delete_confirm(role_id: int):
    roles = RolesService.get_role_by_id(role_id)
    if roles is None:
        abort(404, "Role Not Found")
    form = DeleteRoleForm()
    return render_template("roles/delete.html", role=roles, form=form)

@role_router.route("/<int:role_id>/delete", methods=["POST"])
@login_required
def delete(role_id: int):
    roles = RolesService.get_role_by_id(role_id)
    if roles is None:
        abort(404, "Role Not Found")
    RolesService.delete_role(roles)
    flash(f"Role {roles.name} deleted successfully", "success")
    return redirect(url_for("Role.index"))
