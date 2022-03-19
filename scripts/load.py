import os
import csv
from datetime import datetime
from common.tables import VehicleAll
from common.base import session
from sqlalchemy import text

#base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = os.path.abspath(__file__ + "/../../")
#print(base_path)
transformed_path = f"{base_path}/data/raw/new_vehicle.csv"

def truncate_table():
    """
    Ensure that the tables are in an empty state before running any transformations.
    And primary key (id) restarts from 1.
    """
    session.execute(
        text("TRUNCATE TABLE vehicle ;ALTER SEQUENCE vehicle_id_seq RESTART;")
    )
    session.commit()

def load_new_vehicle_data():
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(transformed_path, mode="r", encoding="windows-1252") as csv_file:
        # Read the new CSV snapshot ready to be processed
        reader = csv.DictReader(csv_file)
        # Initialize an empty list 
        new_objects = []
        for row in reader:
            # Apply transformations and save as object
            new_objects.append(
                VehicleAll(
                    vehicle_spec_id = row['vehicle_spec_id'],
                    year = row['year'],
                    make = row['make'],
                    model = row['model'],
                    drivetrain = row['drivetrain'],
                    max_torque = row['max_torque'],
                    max_horsepower = row['max_horsepower'],
                    max_horsepower_rpm = row['max_horsepower_rpm'],
                    max_torque_rpm = row['max_torque_rpm'],
                    engine_displacement = row['engine_displacement'],
                    fuel_type = row['fuel_type'],
                    fuel_tank_capacity = row['fuel_tank_capacity'],
                    fuel_economy_city = row['fuel_economy_city'],
                    fuel_economy_highway = row['fuel_economy_highway'],
                    cylinders = row['cylinders'],
                    forced_induction = row['forced_induction'],
                    device_generation = row['device_generation']             
                )
            )
        # Save all new processed objects and commit
        session.bulk_save_objects(new_objects)
        session.commit()

def main():
    print("[Load] Start")   
    print("[Load] Truncating table")  
    truncate_table  
    print("[Load] Data going in Postgres...")
    load_new_vehicle_data()
    print("[Load] End")