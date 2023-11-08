import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DBURL")

def create_tables():
    connection = psycopg2.connect(url)

    CREATE_DESTINATIONS_TABLE = (
        "CREATE TABLE IF NOT EXISTS destinations (id SERIAL PRIMARY KEY, name TEXT, description TEXT, location TEXT);"
    )

    CREATE_ITINERARIES_TABLE = (
        "CREATE TABLE IF NOT EXISTS itineraries (id SERIAL PRIMARY KEY, destination_id INT, activity TEXT);"
    )

    CREATE_EXPENSES_TABLE = (
        "CREATE TABLE IF NOT EXISTS expenses (id SERIAL PRIMARY KEY, destination_id INT, expense_category TEXT, amount FLOAT);"
    )

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DESTINATIONS_TABLE)
            cursor.execute(CREATE_ITINERARIES_TABLE)
            cursor.execute(CREATE_EXPENSES_TABLE)

if __name__ == '__main__':
    create_tables()
