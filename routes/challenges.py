from flask import Blueprint, render_template
from flask import session, redirect, url_for
from database.supabase import supabase
challenges_bp = Blueprint(
    "challenges",
    __name__
)
@challenges_bp.route("/challenges")
def challenges():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    progress = (
        supabase
        .table("user_challenges")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    progress_map = {}
    for p in progress.data:
        progress_map[p["challenge_id"]] = p
    daily = (
        supabase
        .table("challenges")
        .select("*")
        .eq("period", "daily")
        .execute()
    )
    weekly = (
        supabase
        .table("challenges")
        .select("*")
        .eq("period", "weekly")
        .execute()
    )
    return render_template(
        "challenges.html",
        daily=daily.data,
        weekly=weekly.data,
        progress=progress_map
    )