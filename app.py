from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    session,
    redirect,
    url_for
)
from dotenv import load_dotenv
from supabase import create_client
import os
import random
from data.paragraphs import (
    easy_paragraphs,
    medium_paragraphs,
    hard_paragraphs
)
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# -------------------------
# SUPABASE
# -------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
# -------------------------
# LOGIN PAGE
# -------------------------
@app.route("/login")
def login():
    return render_template("login.html")
# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("index.html")
# -------------------------
# SET SESSION
# -------------------------
@app.route("/set-session", methods=["POST"])
def set_session():
    data = request.json
    access_token = data.get("access_token")
    if not access_token:
        return jsonify({
            "error": "No token provided"
        }), 400
    user = supabase.auth.get_user(
        access_token
    )
    if not user or not user.user:
        return jsonify({
            "error": "Invalid session"
        }), 401
    session["user"] = user.user.id
    return jsonify({
        "message": "Session created",
        "user_id": user.user.id
    })
@app.route("/create-profile", methods=["POST"])
def create_profile():

    data = request.json

    user_id = data.get("id")
    email = data.get("email")
    full_name = data.get("full_name")

    try:

        existing = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if existing.data:
            return jsonify({
                "message": "Profile already exists"
            })

        result = (
            supabase.table("profiles")
            .insert({
                "id": user_id,
                "email": email,
                "full_name": full_name
            })
            .execute()
        )

        return jsonify({
            "message": "Profile created"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
#   Save Result
@app.route("/save-result", methods=["POST"])
def save_result():

    user_id = session.get("user")

    data = request.json

    print("RECEIVED DATA:")
    print(data)

    try:

        result = (
            supabase.table("typing_results")
            .insert({
                "user_id": user_id,
                "wpm": int(data["wpm"]),
                "accuracy": float(data["accuracy"]),
                "mistakes": int(data["mistakes"]),
                "difficulty": str(data["difficulty"]),
                "achievement": str(data["achievement"])
            })
            .execute()
        )

        print(result)

        return jsonify({
            "message": "Saved"
        })

    except Exception as e:

        print("SAVE RESULT ERROR:")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500
#   Update Stat
@app.route("/update-stats", methods=["POST"])
def update_stats():
    user_id = session.get("user")
    if not user_id:
        return jsonify({
            "error": "Not logged in"
        }), 401
    data = request.json
    wpm = data["wpm"]
    try:
        existing = (
            supabase.table("user_stats")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        if not existing.data:
            supabase.table("user_stats").insert({
                "user_id": user_id,
                "total_tests": 1,
                "best_wpm": wpm,
                "total_xp": wpm,
                "level": 1
            }).execute()
        else:
            stats = existing.data[0]
            total_tests = stats["total_tests"] + 1
            best_wpm = max(stats["best_wpm"], wpm)
            total_xp = stats["total_xp"] + wpm
            level = (total_xp // 500) + 1
            supabase.table("user_stats").update({
                "total_tests": total_tests,
                "best_wpm": best_wpm,
                "total_xp": total_xp,
                "level": level
            }).eq(
                "user_id",
                user_id
            ).execute()
        return jsonify({
            "message": "Stats updated"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# -------------------------
# CURRENT USER
# -------------------------
@app.route("/me")
def me():
    user_id = session.get("user")
    if not user_id:
        return jsonify({
            "error": "Not logged in"
        }), 401
    return jsonify({
        "user_id": user_id
    })
# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        url_for("login")
    )
# -------------------------
# PARAGRAPH API
# -------------------------
@app.route("/get-paragraph/<difficulty>")
def get_paragraph(difficulty):
    if difficulty == "Easy":
        paragraph = random.choice(
            easy_paragraphs
        )
    elif difficulty == "Medium":
        paragraph = random.choice(
            medium_paragraphs
        )
    else:
        paragraph = random.choice(
            hard_paragraphs
        )
    return jsonify({
        "paragraph": paragraph
    })
if __name__ == "__main__":
    app.run(debug=True)