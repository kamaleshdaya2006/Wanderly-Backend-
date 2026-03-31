import os
import psycopg2

conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)
