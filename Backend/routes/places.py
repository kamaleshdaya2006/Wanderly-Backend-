from flask import Blueprint, jsonify, request
from db import get_connection

places_bp = Blueprint("places", __name__)

@places_bp.route("/", methods=["GET"])
def get_places():
    category = request.args.get("category")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if category:
            cursor.execute("""
                SELECT place_id, name, description, image, category
                FROM places
                WHERE LOWER(category) = LOWER(%s)
            """, (category,))
        else:
            cursor.execute("""
                SELECT place_id, name, description, image, category
                FROM places
            """)

        return jsonify([
            {
                "place_id": r[0],
                "name": r[1],
                "description": r[2] or "",
                "image": r[3],
                "category": r[4]
            }
            for r in cursor.fetchall()
        ])

    finally:
        cursor.close()
        conn.close()


@places_bp.route("/<int:place_id>", methods=["GET"])
def get_place(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT place_id, name, description, image, category
            FROM places
            WHERE place_id = %s
        """, (place_id,))

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Not found"}), 404

        return jsonify({
            "place": {
                "place_id": row[0],
                "name": row[1],
                "description": row[2] or "",
                "image": row[3],
                "category": row[4]
            }
        })

    finally:
        cursor.close()
        conn.close()


@places_bp.route("/", methods=["POST"])
def add_place():
    data = request.json

    if not data.get("name"):
        return jsonify({"error": "Name required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO places (name, description, category)
        VALUES (%s, %s, %s)
    """, (
        data["name"],
        data.get("description"),
        data.get("category")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Place added"}), 201
# ----------------------------------------------------
# SEARCH PLACES
# ----------------------------------------------------
@places_bp.route("/search", methods=["GET"])
def search_places():
    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT place_id, name, description, image
            FROM places
            WHERE LOWER(name) LIKE %s
            LIMIT 10
        """, (f"%{query}%",))

        results = [
            {
                "place_id": row[0],
                "name": row[1],
                "description": row[2] or "",
                "image": row[3]
            }
            for row in cursor.fetchall()
        ]

        return jsonify(results)

    finally:
        cursor.close()
        conn.close()
