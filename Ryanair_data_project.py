import mysql.connector
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# MySQL config
config = {
    "user": "root",
    "password": "mySQLprogrammingclass_25",
    "host": "localhost",
    "database": "ryanair_db",
}

def connect_db():
    return mysql.connector.connect(**config)

def generate_flight_operations_data(num_airports=10, num_aircrafts=5, num_flights=100):
    random.seed(42)
    np.random.seed(42)

    cities = ["Dublin", "London", "Madrid", "Berlin", "Rome", "Paris", "Lisbon", "Vienna", "Warsaw", "Prague"]
    countries = ["Ireland", "UK", "Spain", "Germany", "Italy", "France", "Portugal", "Austria", "Poland", "Czechia"]
    aircraft_models = ["Boeing 737", "Airbus A320", "Boeing 737 MAX", "Airbus A321", "Embraer E190"]
    statuses = ["on time", "delayed", "cancelled"]

    # Airports
    airports = []
    for i in range(num_airports):
        airport_id = i + 1
        city = cities[i % len(cities)]
        country = countries[i % len(countries)]
        name = f"{city} International Airport"
        iata_code = city[:3].upper()
        airports.append([airport_id, name, city, country, iata_code])
    df_airport = pd.DataFrame(airports, columns=["airport_id", "name", "city", "country", "iata_code"])

    # Aircraft
    aircraft = []
    for i in range(num_aircrafts):
        aircraft_id = i + 1
        model = aircraft_models[i % len(aircraft_models)]
        capacity = random.choice([180, 190, 200])
        range_km = random.choice([3500, 2000, 5000])
        aircraft.append([aircraft_id, model, capacity, range_km])
    df_aircraft = pd.DataFrame(aircraft, columns=["aircraft_id", "model", "capacity", "range_km"])

    # Flights
    now = datetime.now()
    flights = []
    for i in range(num_flights):
        flight_id = i + 1
        origin, destination = np.random.choice(df_airport["iata_code"], 2, replace=False)
        departure_time = now + timedelta(hours=random.randint(0, 1000))
        delay = random.choice([0, 0, 15, 30, 60])
        arrival_time = departure_time + timedelta(hours=random.randint(2, 5), minutes=delay)
        aircraft_id = np.random.choice(df_aircraft["aircraft_id"])
        status = np.random.choice(statuses, p=[0.7, 0.25, 0.05])
        flights.append([
            flight_id, origin, destination,
            departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            aircraft_id, status
        ])
    df_flights = pd.DataFrame(flights, columns=[
        "flight_id", "origin", "destination", "departure_time",
        "arrival_time", "aircraft_id", "status"
    ])

    return df_airport, df_aircraft, df_flights

# Insert rows
def insert_airports(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO airports (airport_id, name, city, country, iata_code)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(row))

def insert_aircraft(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO aircraft (aircraft_id, model, capacity, range_km)
            VALUES (%s, %s, %s, %s)
        """, tuple(row))

def insert_flights(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO flights (flight_id, origin, destination, departure_time, arrival_time, aircraft_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))

def main():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM airports")
        airport_count = cursor.fetchone()[0]
        if airport_count == 0:
            print("Inserting airports and aircraft...")
            airports, aircraft, _ = generate_flight_operations_data(num_airports=10, num_aircrafts=5, num_flights=0)
            insert_airports(cursor, airports)
            insert_aircraft(cursor, aircraft)
        else:
            print("Airports and aircraft already exist, skipping...")

        cursor.execute("SELECT MAX(flight_id) FROM flights")
        result = cursor.fetchone()
        start_id = result[0] + 1 if result[0] is not None else 1

        print("Inserting new flight batch...")
        _, _, flights = generate_flight_operations_data(num_airports=10, num_aircrafts=5, num_flights=100)
        flights["flight_id"] = range(start_id, start_id + len(flights))
        insert_flights(cursor, flights)

        conn.commit()
        print("Data added successfully.")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()


