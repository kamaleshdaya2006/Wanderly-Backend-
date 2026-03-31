import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        os.getenv("postgresql://postgres:Invulnerabl@db.gvtruqnydrtiyqupguiu.supabase.co:5432/postgres")
    )   