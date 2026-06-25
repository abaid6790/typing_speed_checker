from database.supabase import supabase
def unlock_achievement(user_id, name, badge):
    existing = (
        supabase
        .table("achievements")
        .select("*")
        .eq("user_id", user_id)
        .eq("achievement_name", name)
        .execute()
    )
    if existing.data:
        return
    supabase.table(
        "achievements"
    ).insert({
        "user_id": user_id,
        "achievement_name": name,
        "badge": badge
    }).execute()
def check_achievements(user_id):
    stats = (
        supabase
        .table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    if not stats.data:
        return
    user = stats.data[0]
    tests = user["total_tests"]
    best_wpm = user["best_wpm"]
    accuracy = user["highest_accuracy"]
    if tests >= 1:
        unlock_achievement(
            user_id,
            "First Test",
            "Bronze"
        )
    if tests >= 1:
        unlock_achievement(
            user_id,
            "First Test",
            "Bronze"
        )
    if tests >= 5:
        unlock_achievement(
            user_id,
            "5 Tests Completed",
            "Bronze"
        )
    if tests >= 10:
        unlock_achievement(
            user_id,
            "10 Tests Completed",
            "Silver"
        )
    if best_wpm >= 50:
        unlock_achievement(
            user_id,
            "Fast Typist",
            "Silver"
        )
    if best_wpm >= 80:
        unlock_achievement(
            user_id,
            "Speed Demon",
            "Gold"
        )
    if accuracy >= 95:
        unlock_achievement(
            user_id,
            "Accuracy Master",
            "Gold"
        )