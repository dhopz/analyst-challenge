from datetime import datetime
import os
import sys
import xlsxwriter

sys.path.append('..')
from common.base import session
from common.tables import DriveAll
# Settings
base_path = os.path.abspath(__file__ + "/../../../")
ref_month = datetime.today().strftime("%Y-%m")

if __name__ == "__main__":
    data = session.execute(
        '''SELECT * FROM drive
        WHERE trip_id = '00922df3be5a4589ab385d0c2da2dd81';'''
        ).all()
    
    # Create the workbook
    workbook = xlsxwriter.Workbook(
        f"{base_path}/data/insights/SingleTripId.xlsx"
    )
    
    # Add a new worksheet
    worksheet = workbook.add_worksheet()
    worksheet.set_column("A:L", 12)

    #print(data)
    
    # Add the table with all results in the newly created worksheet
    worksheet.add_table(
        "A2:L2900",
        {
            "data": data,
            "columns": [
                {"header": 'id'},
                {"header": 'trip_id'},
                {"header": 'datetime'},
                {"header": 'vehicle_spec_id'},
                {"header": 'engine_coolant_temp'},
                {"header": 'eng_load'},
                {"header": 'fuel_level'},
                {"header": 'iat'},
                {"header": 'rpm'},
                {"header": 'lat'},
                {"header": 'long'},
                {"header": 'velocity'},
            ],
        },
    )
    workbook.close()
    
    print("Data exported:",  f"{base_path}/data/insights/SingleTripId.xlsx")