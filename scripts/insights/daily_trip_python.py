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

def create_dataframe():
    data = session.execute(
        '''
        SELECT datetime, trip_id, make, model, lat, long, velocity
        FROM drive
        INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id;'''
        ).all()

    df = pd.DataFrame(data, columns=['Datetime','trip_id','make','model','lat','long','velocity'])

    return df

def calc_distance_using_lat_long():
    df = create_dataframe()

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

    #Applying Distancer to each row, could probably do Vectorisation
    df['distance'] = df.apply(distancer, axis=1)

    #Import into SQL
    conn = engine.connect()
    df.to_sql('daily_trip_long_lat_calc', conn, if_exists='replace')
    print("Dataframe lat and lon calculation exported to PSQL")


def calc_distance_using_velocity():
    df = create_dataframe()

    #Converts UTC to Pacific standard time
    df['Datetime'] = df['Datetime'].dt.tz_localize('utc').dt.tz_convert('US/Pacific')

    #Change dataframe to get the difference between the timestamps
    df['timeMax'] = df.groupby(df['trip_id'])['Datetime'].transform('max')
    df['timeMin'] = df.groupby(df['trip_id'])['Datetime'].transform('min')
    df['trip_duration_minutes'] = round((df['timeMax'] - df['timeMin'])/np.timedelta64(1,'m'))

    #Groupby to get average velocity over the trip_id
    df = df.groupby(['trip_id','make','model','trip_duration_minutes'])['velocity'].mean().reset_index()
    df = df.rename(columns={'velocity':'average_velocity'})

    #Calculate distance travelled
    df['distance_travelled'] = (df['trip_duration_minutes']/60) * df['average_velocity']

    #Import into SQL
    conn = engine.connect()
    df.to_sql('daily_trip_velocity_calc', conn, if_exists='replace')
    print("Dataframe velocity calculation exported to PSQL")


if __name__ == "__main__":
    calc_distance_using_lat_long()
    calc_distance_using_velocity()
    print('[Load] Dataframes to PSQL')
