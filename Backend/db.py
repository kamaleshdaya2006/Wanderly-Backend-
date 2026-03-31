import os
import psycopg2

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    print("DB URL:", db_url)  # debug

    return psycopg2.connect(
        db_url,
        sslmode="require"
    )
