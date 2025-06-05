import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Blueprint, request, jsonify
import bcrypt
from database.connection import get_connection
import psycopg2
auth = Blueprint('auth', __name__)


@auth.route('/api/price-trends')
def price_trends():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT scraped_date::date, 
               ROUND(AVG(REPLACE(REPLACE(property_price, '$', ''), ',', '')::numeric), 1) AS avg_price
        FROM zillow_scraped_data
        GROUP BY scraped_date::date
        ORDER BY scraped_date::date ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    trends = [{"date": str(row[0]), "average": float(row[1])} for row in data]
    return jsonify(trends)

@auth.route('/api/total-listings', methods=['GET'])
def total_listings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM zillow_scraped_data")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"totalListings": result[0]})

def get_average_price():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT AVG(REPLACE(REPLACE(property_price, '$', ''), ',', '')::numeric)
        FROM zillow_scraped_data
    """
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return float(result[0]) if result[0] is not None else 0.0

@auth.route('/api/average-price', methods=['GET'])
def average_price():
    price = get_average_price()
    return jsonify({'averagePrice': price})

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Invalid email or password"}), 401

        hashed_password = result[0]

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not email or not name or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)

        # Insert user
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """, (name, email, hashed_password))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'User registered successfully'}), 201

    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
