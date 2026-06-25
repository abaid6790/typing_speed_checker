from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request

from database.supabase import supabase

profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    profile_result = (
        supabase
        .table("profiles")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    stats_result = (
        supabase
        .table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if profile_result.data:
        profile_data = profile_result.data[0]
    else:
        profile_data = {
            "full_name": "No Name",
            "email": session.get("email", ""),
            "created_at": "2026-01-01"
        }

    if stats_result.data:
        stats_data = stats_result.data[0]
    else:
        stats_data = {
            "level": 1,
            "total_xp": 0,
            "total_tests": 0,
            "best_wpm": 0
        }

    return render_template(
        "profile.html",
        profile=profile_data,
        stats=stats_data
    )


@profile_bp.route(
    "/update-profile",
    methods=["POST"]
)
def update_profile():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    full_name = request.form.get(
        "full_name"
    )

    supabase.table(
        "profiles"
    ).update({
        "full_name": full_name
    }).eq(
        "id",
        user_id
    ).execute()

    return redirect("/profile")