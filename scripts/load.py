import os
import csv
from datetime import datetime
from common.tables import VehicleAll, DriveAll
from common.base import session, engine
from sqlalchemy import text
import pandas as pd

#base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = os.path.abspath(__file__ + "/../../")
#print(base_path)
vehicle_path = f"{base_path}/data/raw/new_vehicle.csv"
drive_path = f"{base_path}/data/raw/new_drive.csv"

def truncate_vehicle_table():
    session.execute(
        text("TRUNCATE TABLE vehicle ;ALTER SEQUENCE vehicle_id_seq RESTART;"))
    session.commit()
    print('[Load] Vehicle Table truncated')

def truncate_drive_table():
    session.execute(
        text("TRUNCATE TABLE drive ;ALTER SEQUENCE drive_id_seq RESTART;"))
    session.commit()
    print("['Load'] Drive table Truncated")

def load_new_vehicle_data():
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    df = pd.read_csv(vehicle_path)
    conn = engine.connect()
    df.to_sql('vehicle', conn, if_exists='replace')

def load_new_drive_data():
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(drive_path, mode="r", encoding="windows-1252") as csv_file:
        # Read the new CSV snapshot ready to be processed
        reader = csv.DictReader(csv_file)
        # Initialize an empty list 
        new_objects = []
        for row in reader:
            # Apply transformations and save as object
            new_objects.append(
                DriveAll(
                    trip_id = row['trip_id'],
                    datetime = row['datetime'],
                    vehicle_spec_id = row['vehicle_spec_id'],
                    engine_coolant_temp = row['engine_coolant_temp'],
                    eng_load = row['eng_load'],
                    fuel_level = row['fuel_level'],
                    iat = row['iat'],
                    rpm = row['rpm'],
                    lat = row['lat'],
                    long = row['long'],
                    velocity = row['velocity']          
                )
            )
        # Save all new processed objects and commit
        session.bulk_save_objects(new_objects)
        session.commit()

def main():
    print("[Load] Start")   
    print("[Load] Truncating table")  
    truncate_vehicle_table  
    truncate_drive_table
    print("[Load] Data going in Postgres...")
    load_new_vehicle_data()
    print('[Load] Vehicle Data complete')
    load_new_drive_data()
    print('[Load] Drive data complete')
    print("[Load] End")