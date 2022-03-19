from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')

engine = create_engine("postgresql+psycopg2://"+DATABASE_USERNAME+":postgres@localhost/analyst_challenge")
# Initialize the session
session = Session(engine)
query = """
CREATE TABLE vehicle (
    vehicle_spec_id INT PRIMARY KEY,
    year INT,
    make VARCHAR (50),
    Model VARCHAR (50),
    drivetrain INT,
    max_torque INT,
    max_horsepower INT,
    max_horsepower_rpm INT,
    max_torque_rpm INT,
    engine_displacement DECIMAL,
    fuel_type INT,
    fuel_tank_capacity INT,
    fuel_economy_city DECIMAL,
    fuel_economy_highway DECIMAL,
    cylinders INT,
    forced_induction INT DEFAULT NULL,
    device_generation INT,
    UNIQUE (vehicle_spec_id)
    );

CREATE TABLE drive (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR (50),
    datetime TIMESTAMP NOT NULL,
    vehicle_spec_id INT,
    engine_coolant_temp INT,
    eng_load INT,
    fuel_level INT,
    iat INT,
    rpm INT,
    lat INT,
    long INT,
    velocity INT,
    CONSTRAINT fk_vehicle_spec_id
        FOREIGN KEY(vehicle_spec_id) 
            REFERENCES vehicle(vehicle_spec_id)
    );

"""

session.execute(query)
session.commit()