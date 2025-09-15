"""
Global Configuration for Application
"""

import logging
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error

# Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


#Loading environmental variables
load_dotenv()


# def get_db_connection():
#     """Establishes and returns a database connection"""
#     try:
#         conn = psycopg2.connect(
#             host=os.getenv("DB_CONNECT_HOST"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             port=os.getenv("DB_PORT"),
#             dbname=os.getenv("DB_NAME"),
#         )
#         logging.info("Successfully connected to database!")
#         return conn
#     except Error as err:
#         logging.error(f"Database connection failed: {err}")
#         raise

#Connection to postgres using sqlalchemy
class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_CONNECT_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

