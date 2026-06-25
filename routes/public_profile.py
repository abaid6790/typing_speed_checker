from flask import Blueprint
from flask import render_template

from database.supabase import supabase

public_profile_bp = Blueprint(
    "public_profile",
    __name__
)


@public_profile_bp.route(
    "/user/<user_id>"
)
def public_profile(user_id):

    profile = (
        supabase
        .table("profiles")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    stats = (
        supabase
        .table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    achievements = (
        supabase
        .table("achievements")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if not stats.data:
        return "User Not Found"

    return render_template(
        "public_profile.html",
        profile=profile.data[0]
        if profile.data else {},
        stats=stats.data[0],
        achievements=achievements.data
    )