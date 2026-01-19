from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app.services.permissions import PermissionService
from app.forms.permissions import CreatePermissionForm, UpdatePermissionForm, DeletePermissionForm

permission_router = Blueprint("Permission", __name__, url_prefix="/permission")

@permission_router.route("/")
@login_required
def index():
    permissions = PermissionService.get_permission_all()
    return render_template("permissions/index.html", permissions=permissions)

@permission_router.route("/<int: permission_id>")   
@login_required
def detail(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)
    if permission is None:
        abort(404, "Permission Not Found")
    
    return render_template("permissions/detail.html", permission=permission)

@permission_router.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreatePermissionForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "code": form.code.data,
            "description": form.description.data
        }
        module_id = form.module_id.data or []
        permission = PermissionService.create_permission(data, module_id)
        flash(f"Permission {permission.name} created successfully", "success")
        return redirect(url_for("permissions.index"))
    return render_template("permissions/create.html", form=form)

@permission_router.route("/<int: permission_id>/edit", methods=["GET", "POST"])
@login_required
def edit(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)
    if permission is None:
        abort(404, "Permission Not Found")
    
    form = UpdatePermissionForm(original_permission=permission, obj=permission)
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "code": form.code.data,
            "description": form.description.data
        }
        module_id = form.module_id.data or []
        PermissionService.update_permission(data, permission, module_id)
        flash(f"Permission {permission.name} updated successfully", "success")
        return redirect(url_for("permissions.detail", permission_id=permission.id))
    return render_template("permissions/edit.html", form=form, permission=permission)

@permission_router.route("/<int: permission_id>/delete", methods=["GET"])
@login_required
def delete_confirm(permission_id: int):

    permission = PermissionService.get_permission_by_id(permission_id)
    if permission is None:
        abort(404, "Permission Not Found")

    form = DeletePermissionForm()
    return render_template("permissions/delete.html", permission=permission, form=form)

@permission_router.route("/<int: permission_id>/delete", methods=["POST"])
@login_required
def delete(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)
    if permission is None:
        abort(404, "Permission Not Found")
    PermissionService.delete_permission(permission)
    flash(f"Permission {permission.name} deleted successfully", "success")
    return redirect(url_for("permissions.index"))

