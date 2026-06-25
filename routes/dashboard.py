from flask import Blueprint, render_template, session, redirect, url_for
from database.supabase import supabase

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    stats = (
        supabase
        .table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if not stats.data:

        supabase.table("user_stats").insert({
            "user_id": user_id,
            "total_tests": 0,
            "best_wpm": 0,
            "average_wpm": 0,
            "highest_accuracy": 0,
            "total_words": 0,
            "total_xp": 0,
            "level": 1,
            "streak": 0
        }).execute()

        data = {
            "total_tests": 0,
            "best_wpm": 0,
            "average_wpm": 0,
            "highest_accuracy": 0,
            "total_xp": 0,
            "level": 1
        }

    else:
        data = stats.data[0]

    return render_template(
        "dashboard.html",
        stats=data,
        email=session["email"]
    )