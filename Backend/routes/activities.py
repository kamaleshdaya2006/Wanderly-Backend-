from flask import Blueprint, jsonify
from db import get_connection

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/<int:place_id>", methods=["GET"])
def get_activities(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT activity_id, name, description, icon
            FROM activities
            WHERE place_id = %s
        """, (place_id,))

        rows = cursor.fetchall()

        return jsonify([
            {
                "activity_id": r[0],
                "name": r[1],
                "description": r[2],
                "icon": r[3]
            }
            for r in rows
        ])

    finally:
        cursor.close()
        conn.close()
