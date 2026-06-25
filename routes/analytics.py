from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from database.supabase import supabase
analytics_bp = Blueprint(
    "analytics",
    __name__
)
@analytics_bp.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )
    user_id = session["user_id"]
    results = (
        supabase
        .table("typing_results")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at")
        .execute()
    )
    data = results.data
    wpm_data = []
    accuracy_data = []
    labels = []
    for i, result in enumerate(data):
        labels.append(f"Test {i+1}")
        wpm_data.append(
            result["wpm"]
        )
        accuracy_data.append(
            result["accuracy"]
        )
    return render_template(
        "analytics.html",
        labels=labels,
        wpm_data=wpm_data,
        accuracy_data=accuracy_data
    )