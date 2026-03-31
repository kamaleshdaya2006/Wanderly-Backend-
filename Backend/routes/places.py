from flask import Blueprint, jsonify, request
from db import get_connection

places_bp = Blueprint("places", __name__)

# ----------------------------------------------------
# GET ALL PLACES OR BY CATEGORY
# ----------------------------------------------------
@places_bp.route("/places", methods=["GET"])
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

        places = []

        for row in cursor.fetchall():
            places.append({
                "place_id": row[0],
                "name": row[1],
                "description": row[2] if row[2] else "",
                "image": row[3],
                "category": row[4]
            })

        return jsonify(places)

    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------
# GET SINGLE PLACE WITH RELATED DATA
# ----------------------------------------------------
@places_bp.route("/places/<int:place_id>", methods=["GET"])
def get_place(place_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Place Info
        cursor.execute("""
            SELECT place_id, name, description, image, category
            FROM places
            WHERE place_id = %s
        """, (place_id,))

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Place not found"}), 404

        place_data = {
            "place_id": row[0],
            "name": row[1],
            "description": row[2] if row[2] else "",
            "image": row[3],
            "category": row[4]
        }

        # 2️⃣ Foods
        cursor.execute("""
            SELECT food_id, name, description, rating, shop_name
            FROM foods
            WHERE place_id = %s
        """, (place_id,))

        foods = [
            {
                "food_id": f[0],
                "name": f[1],
                "description": f[2] if f[2] else "",
                "rating": float(f[3]) if f[3] else None,
                "shop_name": f[4]
            }
            for f in cursor.fetchall()
        ]

        # 3️⃣ Souvenirs
        cursor.execute("""
            SELECT souvenir_id, name, description, rating, shop_name
            FROM souvenirs
            WHERE place_id = %s
        """, (place_id,))

        souvenirs = [
            {
                "souvenir_id": s[0],
                "name": s[1],
                "description": s[2] if s[2] else "",
                "rating": float(s[3]) if s[3] else None,
                "shop_name": s[4]
            }
            for s in cursor.fetchall()
        ]

        # 4️⃣ Activities
        cursor.execute("""
            SELECT activity_id, name, description, icon
            FROM activities
            WHERE place_id = %s
        """, (place_id,))

        activities = [
            {
                "activity_id": a[0],
                "name": a[1],
                "description": a[2] if a[2] else "",
                "icon": a[3]
            }
            for a in cursor.fetchall()
        ]

        # 5️⃣ Reviews
        cursor.execute("""
            SELECT review_id, rating, review_text, created_at
            FROM reviews
            WHERE place_id = %s
            ORDER BY created_at DESC
        """, (place_id,))

        reviews = [
            {
                "review_id": r[0],
                "rating": r[1],
                "text": r[2] if r[2] else "",
                "created_at": str(r[3])
            }
            for r in cursor.fetchall()
        ]

        return jsonify({
            "place": place_data,
            "foods": foods,
            "souvenirs": souvenirs,
            "activities": activities,
            "reviews": reviews
        })

    finally:
        cursor.close()
        conn.close()
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
@places_bp.route("/places", methods=["POST"])
def add_place():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO places (name, description, category, image,
                            latitude, longitude, created_by, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
    """, (
        data["name"],
        data["description"],
        data["category"],
        data.get("image"),
        data["latitude"],
        data["longitude"],
        data.get("created_by")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Place added"}), 201