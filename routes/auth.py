from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.supabase import supabase
auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
            user = response.user
            if user:
                supabase.table("profiles").insert({
                    "id": user.id,
                    "email": email,
                    "full_name": full_name
                }).execute()
                supabase.table("user_stats").insert({
                    "user_id": user.id
                }).execute()
                flash("Registration successful. Please login.", "success")
                return redirect(url_for("auth.login"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("register.html")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            user = response.user
            session["user_id"] = user.id
            session["email"] = user.email
            return redirect(url_for("dashboard.dashboard"))
        except Exception:
            flash("Invalid credentials", "danger")
    return render_template("login.html")
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))