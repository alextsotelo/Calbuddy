import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

""" This module handles the database connection and provides a function to get a database connection. """

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Test the connection
if __name__ == "__main__":
    connection = get_db_connection()
    if connection:
        print("Successfully connected to CalBuddy database!")
    else:
        print("Failed to connect to CalBuddy database")