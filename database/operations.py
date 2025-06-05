import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.connection import get_connection, release_connection  # adjust import as needed


def create_table_if_not_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zillow_scraped_data (
            scraped_date TEXT,
            status_type TEXT,
            property_detail_url TEXT,
            property_price TEXT,
            property_address TEXT,
            property_city TEXT,
            property_state TEXT,
            property_address_zip_code TEXT,
            bedrooms_available TEXT,
            bathrooms_available TEXT,
            broker_name TEXT,
            property_images JSONB
        );
    """)


def insert_property_data(property_data):
    key_map = {
        "scraped date": "scraped_date",
        "status type": "status_type",
        "property detail url": "property_detail_url",
        "property price": "property_price",
        "property address": "property_address",
        "property city": "property_city",
        "property state": "property_state",
        "property address zip code": "property_address_zip_code",
        "bedrooms available": "bedrooms_available",
        "bathrooms available": "bathrooms_available",
        "broker name": "broker_name",
        "property images": "property_images",
    }
    property_data = {key_map.get(k, k): v for k, v in property_data.items()}

    if isinstance(property_data.get("property_images"), list):
        property_data["property_images"] = json.dumps(property_data["property_images"])

    conn = get_connection()
    cursor = conn.cursor()

    try:
        create_table_if_not_exists(cursor)

        cursor.execute("""
            INSERT INTO zillow_scraped_data (
                scraped_date,
                property_detail_url,
                property_price,
                property_address,
                property_city,
                property_state,
                property_address_zip_code,
                bedrooms_available,
                bathrooms_available,
                broker_name,
                property_images,
                status_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (
            property_data.get("scraped_date"),
            property_data.get("property_detail_url"),
            property_data.get("property_price"),
            property_data.get("property_address"),
            property_data.get("property_city"),
            property_data.get("property_state"),
            property_data.get("property_address_zip_code"),
            property_data.get("bedrooms_available"),
            property_data.get("bathrooms_available"),
            property_data.get("broker_name"),
            property_data.get("property_images"),
            property_data.get("status_type")
        ))

        conn.commit()
        print("[✔] Property inserted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"[✘] Failed to insert property: {e}")

    finally:
        cursor.close()
        release_connection(conn)  # 🟢 This replaces conn.close()