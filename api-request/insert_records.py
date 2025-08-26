from api_request import fetch_data
import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
access_key = os.getenv('API_Access_Key')
api_url = f"http://api.weatherstack.com/current?access_key={access_key}&query=FEZ"

def connect_to_db():
    print("Connecting To The Postgresql Database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="weather_db",
            user="ipman",
            password="ipman42"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database Connection Failed: {e}")
        raise

def create_table(conn):
    print("Creating Table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("Table * dev * Was Created.")
    except psycopg2.Error as e:
        print(f"Failed To Create Table: {e}")
    
def insert_data(conn, data):
        print("Inserting Weather Data Into The Database...")
        try:
            location = data.get('location', {})
            current = data.get('current', {})
            if not location or not current:
                raise ValueError("Required keys Are Not Found: 'location' or 'current'")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.raw_weather_data(
                    city, temperature, weather_descriptions, wind_speed, time, inserted_at, utc_offset
                ) VALUES (%s, %s, %s, %s, %s, NOW(), %s);
                """,(
                location.get('name'),
                current.get('temperature'),
                current.get('weather_descriptions', [None])[0],
                current.get('wind_speed'),
                location.get('localtime'),
                location.get('utc_offset')
            ))
            conn.commit()
            print("Data Successfly Inserted")
        except psycopg2.Error as e:
            print(f"Error Inserting Data Into The Table * dev.raw_weather_data * : {e}")
            raise

def main():
    try:
        data = fetch_data(api_url=api_url)
        conn = connect_to_db()
        create_table(conn=conn)
        insert_data(conn=conn, data=data)
    except Exception as e:
        print(f"An Error Occured During Execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database Connection Are Closed.")
