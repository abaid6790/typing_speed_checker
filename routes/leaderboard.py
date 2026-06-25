from flask import Blueprint
from flask import render_template
from database.supabase import supabase

leaderboard_bp = Blueprint(
    "leaderboard",
    __name__
)


@leaderboard_bp.route("/leaderboard")
def leaderboard():

    users = (
        supabase
        .table("user_stats")
        .select("*")
        .order(
            "best_wpm",
            desc=True
        )
        .limit(20)
        .execute()
    )

    return render_template(
        "leaderboard.html",
        users=users.data
    )