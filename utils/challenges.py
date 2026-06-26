from database.supabase import supabase
def update_challenges(user_id, wpm, accuracy, xp, total_tests, total_xp):
    challenges = (
        supabase
        .table("challenges")
        .select("*")
        .execute()
    )
    for challenge in challenges.data:
        progress = 0
        completed = False
        if challenge["type"] == "tests":
            progress = total_tests
        elif challenge["type"] == "wpm":
            progress = wpm
        elif challenge["type"] == "accuracy":
            progress = accuracy
        elif challenge["type"] == "xp":
            progress = total_xp
        if progress >= challenge["target"]:
            completed = True
        existing = (
            supabase
            .table("user_challenges")
            .select("*")
            .eq("user_id", user_id)
            .eq("challenge_id", challenge["id"])
            .execute()
        )
        if existing.data:
            supabase.table("user_challenges").update({
                "progress": progress,
                "completed": completed
            }).eq(
                "id",
                existing.data[0]["id"]
            ).execute()
        else:
            supabase.table("user_challenges").insert({
                "user_id": user_id,
                "challenge_id": challenge["id"],
                "progress": progress,
                "completed": completed,
                "claimed": False
            }).execute()