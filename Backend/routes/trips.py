from flask import Blueprint, jsonify, request
from db import get_connection

trips_bp = Blueprint("trips", __name__)

@trips_bp.route("/<int:user_id>", methods=["GET"])
def get_trips(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT trip_id, trip_name, days, created_at
        FROM trips
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    trips = [
        {
            "trip_id": t[0],
            "name": t[1],
            "days": t[2],
            "created_at": str(t[3])
        }
        for t in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return jsonify(trips)
@trips_bp.route("/", methods=["POST"])
def create_trip():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trips (user_id, trip_name, days)
        VALUES (%s, %s, %s)
        RETURNING trip_id
    """, (
        data["user_id"],
        data["name"],
        data["days"]
    ))

    trip_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Trip created",
        "trip_id": trip_id
    })
@trips_bp.route("/trip_places", methods=["POST"])
def add_place_to_trip():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trip_places (trip_id, place_id, day_number, order_in_day)
        VALUES (%s, %s, %s, %s)
    """, (
        data["trip_id"],
        data["place_id"],
        data["day_number"],
        data["order_in_day"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Place added to trip"})
