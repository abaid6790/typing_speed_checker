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
            response =supabase.auth.sign_up(
                {
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to":
                    "http://127.0.0.1:5000/login"
                }
            })
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
                flash(
    "Registration successful. Please check your email and verify your account.","success")
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

            # Check email verification
            if not user.email_confirmed_at:

                flash(
                    "Please verify your email before logging in.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            session["user_id"] = user.id
            session["email"] = user.email

            return redirect(
                url_for("dashboard.dashboard")
)
        except Exception:
            flash("Invalid credentials", "danger")
    return render_template("login.html")
@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        try:
            supabase.auth.reset_password_email(
                    email,
                    {
                        "redirect_to": "http://127.0.0.1:5000/reset-password"
                    }
                )
            flash(
                "Password reset email sent."
            )
        except Exception as e:
            flash(str(e))
    return render_template(
        "forgot_password.html"
    )
@auth_bp.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():
    if request.method == "POST":
        password = request.form[
            "password"
        ]
        try:
            supabase.auth.update_user({
                "password": password
            })
            flash(
                "Password updated."
            )
            return redirect(
                url_for(
                    "auth.login"
                )
            )
        except Exception as e:
            flash(str(e))
    return render_template(
        "reset_password.html"
    )
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))