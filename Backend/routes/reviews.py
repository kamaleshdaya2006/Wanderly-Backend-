from flask import Blueprint, jsonify, request
from db import get_connection

reviews_bp = Blueprint("reviews", __name__)



@reviews_bp.route("/", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cursor = conn.cursor()

    entity_type = request.args.get("entity_type")
    entity_id = request.args.get("entity_id")

    cursor.execute("""
        SELECT review_id, user_id, rating, review_text, created_at
        FROM reviews
        WHERE entity_type = %s AND entity_id = %s
        ORDER BY created_at DESC
    """, (entity_type, entity_id))

    reviews = [
        {
            "review_id": r[0],
            "user_id": r[1],
            "rating": r[2],
            "review_text": r[3],
            "created_at": str(r[4])
        }
        for r in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return jsonify(reviews)
@reviews_bp.route("/", methods=["POST"])
def add_review():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews (user_id, rating, review_text, entity_type, entity_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["user_id"],
        data["rating"],
        data["review_text"],
        data["entity_type"],
        data["entity_id"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Review added"})
# ----------------------------------------------------
# GET REVIEWS BY PLACE ID (shortcut for frontend)
# ----------------------------------------------------
@reviews_bp.route("/<int:place_id>", methods=["GET"])
def get_reviews_by_place(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT review_id, user_id, rating, review_text, created_at
            FROM reviews
            WHERE entity_type = 'place' AND entity_id = %s
            ORDER BY created_at DESC
        """, (place_id,))

        reviews = [
            {
                "review_id": r[0],
                "user_id": r[1],
                "rating": r[2],
                "review_text": r[3],
                "created_at": str(r[4])
            }
            for r in cursor.fetchall()
        ]

        return jsonify(reviews)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
