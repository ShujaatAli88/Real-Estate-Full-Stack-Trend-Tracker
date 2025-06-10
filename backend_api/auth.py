import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import (
    Blueprint,
    request,
    jsonify,
    Response, 
    stream_with_context
)
import bcrypt
from database.connection import get_connection,release_connection
import psycopg2
import subprocess
auth = Blueprint('auth', __name__)

crawler_process = None


@auth.route('/api/scraped-data/search')
def search_scraped_data():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT * FROM zillow_scraped_data
            WHERE (%(min_price)s IS NULL OR 
                   REPLACE(REPLACE(property_price, '$', ''), ',', '')::numeric >= %(min_price)s)
              AND (%(max_price)s IS NULL OR 
                   REPLACE(REPLACE(property_price, '$', ''), ',', '')::numeric <= %(max_price)s)
        """

        cur.execute(query, {
            'min_price': min_price,
            'max_price': max_price
        })

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]

        return jsonify(data), 200

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        cur.close()
        release_connection(conn)

@auth.route('/api/scraped-data')
def scraped_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT scraped_date," \
        " status_type, " \
        "property_detail_url, " \
        "property_price, " \
        "property_city,\
        property_state," \
        "property_address_zip_code," \
        "bedrooms_available," \
        "bathrooms_available," \
        "broker_name," \
        "broker_name FROM zillow_scraped_data ORDER BY scraped_date DESC")
        rows = cur.fetchall()
        result = [
            {
                "scraped_date": str(row[0]),
                "status_type": row[1],
                "property_detail_url": row[2],
                "property_price": row[3],
                "property_city": row[4],
                "property_state": row[5],
                "property_address_zip_code" :row[6],
                "bedrooms_available": row[7],
                "bathrooms_available": row[8],
                "broker_name":row[9],
            }
            for row in rows
        ]
        return jsonify(result)
    except Exception as err:
        print(f"Error while fetching Scraped data:{err}")
    finally:
        cur.close()
        release_connection(conn)

@auth.route('/api/stop-crawler', methods=['POST'])
def stop_crawler():
    global crawler_process
    if crawler_process and crawler_process.poll() is None:
        crawler_process.terminate()
        return jsonify({'message': 'Crawler stopped successfully.'})
    return jsonify({'message': 'No crawler is currently running.'}), 400


ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by control sequences
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)

def strip_ansi(text):
    return ansi_escape.sub('', text)

@auth.route('/api/run-crawler', methods=['GET'])
def run_crawler():
    global crawler_process

    if crawler_process and crawler_process.poll() is None:
        return jsonify({'message': 'Crawler is already running.'}), 400

    crawler_process = subprocess.Popen(
        ['python', '../scraper/main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    def generate():
        for line in crawler_process.stdout:
            clean_line = strip_ansi(line)
            yield f"data: {clean_line.strip()}\n\n"
        crawler_process.stdout.close()
        crawler_process.wait()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@auth.route('/api/price-trends')
def price_trends():
    try:
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
    except Exception as err:
        print(f"Error While Getting price-trends:{err}")
    
    finally:
        cursor.close()
        release_connection(conn)

@auth.route('/api/total-listings', methods=['GET'])
def total_listings():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM zillow_scraped_data")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"totalListings": result[0]})
    except Exception as err:
        print(f"Error While getting Total Listings:{err}")
    
    finally:
        cursor.close()
        release_connection(conn)

def get_average_price():
    try:
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
    except Exception as err:
        print(f"Error While Getting Average Price:{err}")
    finally:
        cursor.close()
        release_connection(conn)

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
        cursor.close()
        release_connection(conn)

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
    finally:
        cursor.close()
        release_connection(conn)