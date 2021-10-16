# Trying to put data into the InfluxDB from an csv file
# pip install influxdb

import datetime
import pandas as pd
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('smartgridai')

data = pd.read_csv("2019-ETI-EMON-V01-695FA5-1640EF.txt", index_col='timestamp')

for index, row in data.iterrows():
    data_points = [{
            "measurement": "datasets",
            "tags": {
                "id": "2019-ETI-EMON-V01-695FA5-1640EF",
            },
            "time": index,
            "fields": {
                "consumption_kw": row['consumption_kw'],
                "consumption_t1_kwh": row['consumption_t1_kwh'],
                "consumption_t2_kwh": row['consumption_t2_kwh'],
                "production_kw": row['production_kw'],
                "production_t1_kwh": row['production_t1_kwh'],
                "production_t2_kwh": row['production_t2_kwh']
            }
        }]
    client.write_points(data_points)
    print(".")

print("\nREADY\n")

print("Read data")
result = client.query('SELECT * FROM datasets WHERE id="2019-ETI-EMON-V01-695FA5-1640EF"')
print(result.raw['series'][0]['values'])

