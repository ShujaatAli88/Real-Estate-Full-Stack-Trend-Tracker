import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from psycopg2.pool import SimpleConnectionPool
from database.config import Config

###Setting Database connection parameters using environment variables
DB_CONFIG = {
    "host": Config.DB_HOST,
    "database": Config.DB_NAME,
    "user": Config.DB_USER,
    "password": Config.DB_PASSWORD,
    "port": Config.DB_PORT
}

connection_pool = SimpleConnectionPool(1, 10, **DB_CONFIG)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)
