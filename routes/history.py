from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from database.supabase import supabase
history_bp = Blueprint(
    "history",
    __name__
)
@history_bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )
    user_id = session["user_id"]
    search = request.args.get(
        "search",
        ""
    )
    query = (
        supabase
        .table("typing_results")
        .select("*")
        .eq("user_id", user_id)
        .order(
            "created_at",
            desc=True
        )
    )
    results = query.execute().data
    if search:
        results = [
            r for r in results
            if search.lower()
            in str(r["wpm"]).lower()
        ]
    return render_template(
        "history.html",
        results=results,
        search=search
    )
@history_bp.route(
    "/delete-result/<int:result_id>"
)
def delete_result(result_id):
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )
    supabase.table(
        "typing_results"
    ).delete().eq(
        "id",
        result_id
    ).execute()
    return redirect("/history")