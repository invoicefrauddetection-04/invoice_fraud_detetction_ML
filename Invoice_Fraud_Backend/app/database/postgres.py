import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def get_connection():

    print("DB_HOST =", os.getenv("DB_HOST"))
    print("DB_PORT =", os.getenv("DB_PORT"))
    print("DB_NAME =", os.getenv("DB_NAME"))
    print("DB_USER =", os.getenv("DB_USER")) 

    return psycopg2.connect(

        host=os.getenv("DB_HOST"),

        database=os.getenv("DB_NAME"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

        port=os.getenv("DB_PORT")
    )