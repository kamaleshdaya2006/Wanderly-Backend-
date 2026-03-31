from flask import Blueprint, jsonify, request
from db import get_connection

souvenirs_bp = Blueprint("souvenirs", __name__)

@souvenirs_bp.route("/souvenirs", methods=["GET"])
def get_all_souvenirs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.souvenir_id, s.place_id, s.name, s.description,
               s.rating, s.shop_name, p.name
        FROM souvenirs s
        JOIN places p ON s.place_id = p.place_id
    """)

    souvenirs = [
        {
            "souvenir_id": s[0],
            "place_id": s[1],
            "name": s[2],
            "description": s[3],
            "rating": float(s[4]) if s[4] else None,
            "shop_name": s[5],
            "place_name": s[6]
        }
        for s in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return jsonify(souvenirs)
@souvenirs_bp.route("/souvenirs", methods=["POST"])
def add_souvenir():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO souvenirs (place_id, name, description, rating, shop_name)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["place_id"],
        data["name"],
        data["description"],
        data.get("rating"),
        data.get("shop_name")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Souvenir added"}), 201