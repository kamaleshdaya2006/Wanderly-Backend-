from flask import Blueprint, jsonify, request
from db import get_connection

guides_bp = Blueprint("guides", __name__)

@guides_bp.route("/guides", methods=["GET"])
def get_guides():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT guide_id, name, description, languages,
               rating, price_per_day, image
        FROM guides
    """)

    guides = [
        {
            "guide_id": g[0],
            "name": g[1],
            "description": g[2],
            "languages": g[3],
            "rating": g[4],
            "price": g[5],
            "image": g[6]
        }
        for g in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return jsonify(guides)


@guides_bp.route("/guides", methods=["POST"])
def add_guide():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO guides (name, description, languages,
                            price_per_day, user_id, image, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending')
    """, (
        data["name"],
        data["description"],
        data["languages"],
        data["price"],
        data["user_id"],
        data.get("image")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Guide added"})