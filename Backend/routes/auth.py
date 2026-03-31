from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint("auth", __name__)

# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, name, email, password, city
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "User not found"}), 401

        if password != user[3]:
            return jsonify({"message": "Invalid password"}), 401

        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
            "city": user[4]
        })

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()


# ================= SIGNUP =================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    city = data.get("city")

    if not name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            return jsonify({"message": "Email already registered"}), 400

        cursor.execute("""
            INSERT INTO users (name, email, password, city)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, city))

        conn.commit()

        return jsonify({"message": "Signup successful"}), 201

    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()
