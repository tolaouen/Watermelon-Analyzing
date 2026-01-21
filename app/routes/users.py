from app.services.users import UserService
from flask import Blueprint, render_template, redirect, abort, url_for, flash
from app.forms.users import UserCreateForm, UserUpdateForm, UserDeleteForm
from flask_login import login_required

from extensions import db

user_router = Blueprint("User", __name__, url_prefix="/user")

@user_router.route("/")
@login_required
def index():
    users =  UserService.get_user_all()
    return render_template("users/index.html", users=users)

@user_router.route("/<int:user_id>")
@login_required
def detail(user_id: int):
    user = UserService.get_user_by_id(user_id)

    if user is None:
        abort(404, "User Not Found")
    return render_template("users/detail.html", user=user)

@user_router.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = UserCreateForm()

    if form.validate_on_submit():

        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data if hasattr(form, "is_active") else True,
        }
        password = form.password.data
        role_id = form.role_id.data or None
        users = UserService.create_user(data, password, role_id)
        flash(f"User '{users.username}' was created successfully.", "success")
        return redirect(url_for("User.detail", user_id=users.id))
    return render_template("users/create.html", form=form)

@user_router.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id: int):
    users = UserService.get_user_by_id(user_id)
    if users is None:
        abort(404, "User not found")

    form = UserUpdateForm(original_user=users, obj=users)

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data if hasattr(form, "is_active") else True,
        }
        password = form.password.data or None
        role_id = form.role_id.data or None
        UserService.update_user(users, data, password, role_id)
        flash(f"User '{users.username}' was updated successfully.", "success")
        return redirect(url_for("User.detail", user_id=users.id))
    return render_template("users/edit.html", form=form, user=users)

@user_router.route("/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_confirm(user_id: int):
    users = UserService.get_user_by_id(user_id)
    if users is None:
        abort(404, "User not found")

    form = UserDeleteForm()
    return render_template("users/delete.html", user=users, form=form)

@user_router.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404, "User not found")

    UserService.delete_user(user)
    flash("User was deleted successfully", "success")
    return redirect(url_for("User.index"))




