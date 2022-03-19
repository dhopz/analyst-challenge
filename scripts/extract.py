import os
import csv
import tempfile
from zipfile import ZipFile

import requests

# Settings
base_path = os.path.abspath(__file__ + "/../../")

# Source path where we want to save the .zip file downloaded from the website
source_path = f"{base_path}/data/source/analyst-challenge.zip"

# Raw path where we want to extract the new .csv data
drive_path = f"{base_path}/data/raw/new_drive.csv"
vehicle_path = f"{base_path}/data/raw/new_vehicle.csv"

def create_folder_if_not_exists(path):
    """
    Create a new folder if it doesn't exists
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def save_drive_raw_data():
    """
    Save new raw data from the source
    """
    create_folder_if_not_exists(drive_path)
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(
            source_path,
            "r",
        ) as zipfile:
            #names_list = zipfile.namelist()
            csv_file_path = zipfile.extract('analyst-challenge-data/drive.csv', path=dirpath)
            # Open the CSV file in read mode
            with open(csv_file_path, mode="r", encoding="windows-1252") as csv_file:
                reader = csv.DictReader(csv_file)

                row = next(reader)  # Get first row from reader
                #print("[Extract] First row example:", row)

                # Open the CSV file in write mode
                with open(
                    drive_path,
                    mode="w",
                    encoding="windows-1252"
                ) as csv_file:
                    # Rename field names so they're ready for the next step
                    fieldnames = {
                        'trip_id':'trip_id',
                        'datetime':'datetime',
                        'vehicle_spec_id':'vehicle_spec_id',
                        'engine_coolant_temp':'engine_coolant_temp',
                        'eng_load':'eng_load',
                        'fuel_level':'fuel_level',
                        'iat':'iat',
                        'rpm':'rpm',
                        'lat':'lat',
                        'long':'long',
                        'velocity':'velocity'
                    }
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # Write headers as first line
                    writer.writerow(fieldnames)
                    for row in reader:
                        # Write all rows in file
                        writer.writerow(row)

def save_vehicle_raw_data():
    """
    Save new raw data from the source
    """
    create_folder_if_not_exists(drive_path)
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(
            source_path,
            "r",
        ) as zipfile:
            #names_list = zipfile.namelist()
            csv_file_path = zipfile.extract('analyst-challenge-data/vehicle.csv', path=dirpath)
            # Open the CSV file in read mode
            with open(csv_file_path, mode="r", encoding="windows-1252") as csv_file:
                reader = csv.DictReader(csv_file)

                row = next(reader)  # Get first row from reader
                #print("[Extract] First row example:", row)

                # Open the CSV file in write mode
                with open(
                    vehicle_path,
                    mode="w",
                    encoding="windows-1252"
                ) as csv_file:
                    # Rename field names so they're ready for the next step
                    fieldnames = {
                        'vehicle_spec_id':'vehicle_spec_id',
                        'year':'year',
                        'make':'make',
                        'Model':'model',
                        'drivetrain':'drivetrain',
                        'max_torque':'max_torque',
                        'max_horsepower':'max_horsepower',
                        'max_horsepower_rpm':'max_horsepower_rpm',
                        'max_torque_rpm':'max_torque_rpm',
                        'engine_displacement':'engine_displacement',
                        'fuel_type':'fuel_type',
                        'fuel_tank_capacity':'fuel_tank_capacity',
                        'fuel_economy_city':'fuel_economy_city',
                        'fuel_economy_highway':'fuel_economy_highway',
                        'cylinders':'cylinders',
                        'forced_induction':'forced_induction',
                        'device_generation':'device_generation'                        
                    }
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # Write headers as first line
                    writer.writerow(fieldnames)
                    for row in reader:
                        # Write all rows in file
                        writer.writerow(row)

# Main function called inside the execute.py script
def main():
    print("[Extract] Start")
    print(f"[Extract] Saving data from '{source_path}' to '{drive_path}' and '{vehicle_path}'")
    save_drive_raw_data()
    print("[Extract] Drive data CSV complete")
    save_vehicle_raw_data()
    print("[Extract] Vehicle data CSV complete")
    print(f"[Extract] End")