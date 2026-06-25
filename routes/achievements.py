from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from database.supabase import supabase
achievements_bp = Blueprint(
    "achievements",
    __name__)
@achievements_bp.route("/achievements")
def achievements():
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )
    user_id = session["user_id"]
    data = (
        supabase
        .table("achievements")
        .select("*")
        .eq("user_id", user_id)
        .order(
            "unlocked_at",
            desc=True
        )
        .execute()
    )
    return render_template(
        "achievements.html",
        achievements=data.data
    )