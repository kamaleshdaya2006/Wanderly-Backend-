from flask import Blueprint, jsonify
from db import get_connection

hidden_gems_bp = Blueprint("hidden_gems", __name__)

@hidden_gems_bp.route("/hidden-gems", methods=["GET"])
def get_hidden_gems():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT place_id, name, description, image, category
        FROM places
        WHERE LOWER(category) = 'hidden'
    """)

    places = [
        {
            "place_id": r[0],
            "name": r[1],
            "description": r[2],
            "image": r[3],
            "category": r[4]
        }
        for r in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return jsonify(places)