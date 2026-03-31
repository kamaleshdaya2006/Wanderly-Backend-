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
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(places_bp)
app.register_blueprint(foods_bp)
app.register_blueprint(guides_bp)
app.register_blueprint(souvenirs_bp)
app.register_blueprint(hidden_gems_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(reviews_bp)

@app.route("/")
def home():
    return "Backend running"

if __name__ == "__main__":
    app.run()