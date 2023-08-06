import psycopg2
from config import db_config

# Function to connect to the database
def connect():
    try:
        conn = psycopg2.connect(**db_config)
        conn.set_client_encoding('UTF8')  # Add this line to set UTF-8 support
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
