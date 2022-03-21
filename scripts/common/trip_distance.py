from datetime import datetime
import os

from base import session
from tables import DriveAll
import xlsxwriter
import pandas as pd

# Settings
base_path = os.path.abspath(__file__ + "/../../../")
ref_month = datetime.today().strftime("%Y-%m")

if __name__ == "__main__":
    data = session.execute(
        '''SELECT datetime, trip_id, make, model, lat, long, CONCAT(lat, ',',long) as coordinates
        FROM drive
        INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id'''
        ).all()

    df = pd.read_sql(data,session)
        
    