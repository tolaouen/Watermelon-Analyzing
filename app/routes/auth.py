from flask import Blueprint, flash, Flask, abort, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app.models.users import User
from app.models.roles import Role
from app.services.users import UserService

auth_route = Blueprint("auth", __name__, url_prefix="/auth")

@auth_route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.is_active:
                flash("Your account is inactive. Please contact administrator", "warning")
                return redirect(url_for("auth.login"))
            
            login_user(user)
            flash("Logged in successfully", "success")

            return redirect(url_for("users.index"))
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth.login"))
    return render_template("auth/login.html")

@auth_route.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        errors = []

        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if username and User.query.filter_by(username=username).first():
            errors.append("Username already exists")
        if email and UserWarning.query.filter_by(email=email).first():
            errors.append("Email already exists")
        
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("auth/register.html", username=username, email=email, full_name=full_name)
        
        default_role = Role.query.filter_by(name="User").first()
        default_role_id = default_role.id if default_role else None

        data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "is_active": True
        }

        new_user = UserService.create_user(
            data = data,
            password = password,
            role_id = default_role_id
        )

        login_user(new_user)
        flash("Registration successful", "success")
        return redirect(url_for("users.index"))
    return render_template("auth/register.html")

@auth_route.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))



    



        

