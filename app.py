from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.typing import typing_bp
from routes.history import history_bp
from routes.analytics import analytics_bp
from routes.achievements import achievements_bp
from routes.profile import profile_bp
from routes.leaderboard import leaderboard_bp
from routes.challenges import challenges_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(typing_bp)
app.register_blueprint(history_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(challenges_bp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )