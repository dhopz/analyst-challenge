#from .common import base
import pandas as pd
import numpy as np
import geopy.distance
import os
import sys

sys.path.append('..')
from common.base import session, engine
base_path = os.path.abspath(__file__ + "/../../../")

def distancer(row):
    coords_1 = (row['lat'], row['long'])
    coords_2 = (row['next_lat'], row['next_long'])
    return geopy.distance.distance(coords_1, coords_2).km

if __name__ == "__main__":
    #Extract data from database
    data = session.execute(
        '''SELECT datetime, trip_id, make, model, lat, long
        FROM drive
        INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id'''
        ).all()

    #Create Dataframe 
    df = pd.DataFrame(data, columns=['Datetime','trip_id','make','model','lat','long'])
    #Manipulate data to get distance travelled using function Distancer 
    df['next_lat'] = df.groupby('trip_id')['lat'].shift(1)
    df['next_long'] = df.groupby('trip_id')['long'].shift(1)
    df['next_lat'].fillna(df['lat'], inplace=True)
    df['next_long'].fillna(df['long'], inplace=True)

    #Converts UTC to Pacific standard time
    df['Datetime'] = df['Datetime'].dt.tz_localize('utc').dt.tz_convert('US/Pacific')

    #Change dataframe to get the difference between the timestamps
    df['timestamp_end'] = df.groupby('trip_id')['Datetime'].shift(1)
    df['trip_duration_minutes'] = (df['Datetime'] - df['timestamp_end'])/np.timedelta64(1,'m')
    df['timestamp_end'].fillna(df['Datetime'], inplace=True)
    df['trip_duration_minutes'].fillna(0,inplace=True)

    df['distance'] = df.apply(distancer, axis=1)

    conn = engine.connect()
    df.to_sql('daily_trip', conn, if_exists='replace')


    # df.to_excel(f"{base_path}/data/insights/DailyTrip.xlsx")
    # print("Dataframe exported")