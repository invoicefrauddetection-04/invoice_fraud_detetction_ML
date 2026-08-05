import psycopg2
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)
from app.pipeline_DB.database.scripts.db_config import DB_CONFIG


def get_connection():

    return psycopg2.connect(

        host=DB_CONFIG["host"],

        database=DB_CONFIG["database"],

        user=DB_CONFIG["user"],

        password=DB_CONFIG["password"],

        port=DB_CONFIG["port"]

    )