from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint("auth", __name__)

# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ PostgreSQL syntax (%s)
    cursor.execute("""
        SELECT user_id, name, email, password, city
        FROM users
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"message": "User not found"}), 401

    db_password = user[3]

    if password != db_password:
        cursor.close()
        conn.close()
        return jsonify({"message": "Invalid password"}), 401

    result = {
        "message": "Login successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2],
        "city": user[4]
    }

    cursor.close()
    conn.close()

    return jsonify(result)


# ================= SIGNUP =================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    city = data.get("city")

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Check if email exists
    cursor.execute(
        "SELECT user_id FROM users WHERE email = %s",
        (email,)
    )

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Email already registered"}), 400

    # ✅ Insert user (NO sequences needed)
    cursor.execute("""
        INSERT INTO users (name, email, password, city)
        VALUES (%s, %s, %s, %s)
    """, (name, email, password, city))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Signup successful"})