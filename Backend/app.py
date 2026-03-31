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

# ✅ STRONG CORS FIX (production safe)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# ✅ EXTRA HEADERS (fix preflight issues)
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


# =========================
# BLUEPRINTS WITH PREFIX
# =========================
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(places_bp, url_prefix="/places")
app.register_blueprint(foods_bp, url_prefix="/foods")
app.register_blueprint(guides_bp, url_prefix="/guides")
app.register_blueprint(souvenirs_bp, url_prefix="/souvenirs")
app.register_blueprint(hidden_gems_bp, url_prefix="/hidden-gems")
app.register_blueprint(trips_bp, url_prefix="/trips")
app.register_blueprint(reviews_bp, url_prefix="/reviews")


# =========================
# HEALTH CHECK
# =========================
@app.route("/")
def home():
    return "Backend running"


# =========================
# HANDLE PREFLIGHT (VERY IMPORTANT)
# =========================
@app.route("/auth/login", methods=["OPTIONS"])
@app.route("/auth/signup", methods=["OPTIONS"])
def handle_options():
    return "", 200


if __name__ == "__main__":
    app.run()
