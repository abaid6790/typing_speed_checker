from flask import Blueprint, render_template, session, redirect, url_for
from flask import request, jsonify
from database.supabase import supabase
from utils.achievements import check_achievements
import random
from data.easy import paragraphs as easy
from data.medium import paragraphs as medium
from data.hard import paragraphs as hard
typing_bp = Blueprint("typing", __name__)
@typing_bp.route("/typing")
def typing_test():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    difficulty = request.args.get("difficulty", "easy")
    if difficulty == "medium":
        paragraph = random.choice(medium)
    elif difficulty == "hard":
        paragraph = random.choice(hard)
    else:
        paragraph = random.choice(easy)
    timer = request.args.get("timer", 60)
    return render_template(
        "typing_test.html",
        paragraph=paragraph,
        difficulty=difficulty,
        timer=timer    )
@typing_bp.route("/save-result", methods=["POST"])
def save_result():
    if "user_id" not in session:
        return jsonify({"success": False})
    data = request.json
    user_id = session["user_id"]
    wpm = data["wpm"]
    accuracy = data["accuracy"]
    mistakes = data["mistakes"]
    difficulty = data["difficulty"]
    duration = data["duration"]
    xp = int(wpm)
    supabase.table("typing_results").insert({
        "user_id": user_id,
        "wpm": wpm,
        "accuracy": accuracy,
        "mistakes": mistakes,
        "difficulty": difficulty,
        "duration": duration,
        "xp_earned": xp
    }).execute()
    stats = (
        supabase
        .table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    current = stats.data[0]
    total_tests = current["total_tests"] + 1
    from datetime import date
    today = str(date.today())
    streak = current.get("streak", 0)
    last_date = current.get("last_test_date")
    if last_date:
        from datetime import datetime
        last = datetime.strptime(
            str(last_date),
            "%Y-%m-%d"
        ).date()
        current_date = date.today()
        difference = (
            current_date - last
        ).days
        if difference == 1:
            streak += 1
        elif difference > 1:
            streak = 1
    else:
        streak = 1
    best_wpm = max(current["best_wpm"], wpm)
    highest_accuracy = max(
        current["highest_accuracy"],
        accuracy
    )
    total_xp = current["total_xp"] + xp
    average_wpm = (
        (
            current["average_wpm"]
            * current["total_tests"]
        )
        + wpm
    ) / total_tests
    level = (total_xp // 100) + 1
    supabase.table("user_stats").update({
    "total_tests": total_tests,
    "best_wpm": best_wpm,
    "highest_accuracy": highest_accuracy,
    "average_wpm": round(average_wpm),
    "total_xp": total_xp,
    "level": level
    }).eq(
        "user_id",
        user_id
    ).execute()
    check_achievements(user_id)
    return jsonify({"success": True})