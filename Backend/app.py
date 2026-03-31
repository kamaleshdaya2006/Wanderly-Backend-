from flask import Flask
from flask_cors import CORS

from routes.places import places_bp
from routes.auth import auth_bp
from routes.guides import guides_bp
from routes.foods import foods_bp
from routes.souvenirs import souvenirs_bp
from routes.hiddengems import hidden_gems_bp
from routes.trips import trips_bp
from routes.reviews import reviews_bp

app = Flask(__name__)

# ✅ FIXED CORS (ONLY THIS)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False
)
# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(places_bp, url_prefix="/places")
app.register_blueprint(foods_bp, url_prefix="/foods")
app.register_blueprint(guides_bp, url_prefix="/guides")
app.register_blueprint(souvenirs_bp, url_prefix="/souvenirs")
app.register_blueprint(hidden_gems_bp, url_prefix="/hidden-gems")
app.register_blueprint(trips_bp, url_prefix="/trips")
app.register_blueprint(reviews_bp, url_prefix="/reviews")

@app.route("/")
def home():
    return "Backend running"

if __name__ == "__main__":
    app.run()
