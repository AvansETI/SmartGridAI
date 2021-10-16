# Trying to read InfluxDB data into a dataframe pandas
# pip install influxdb

import argparse
import pandas as pd

from influxdb import DataFrameClient

import pandas as pd

client = DataFrameClient(host='localhost', port=8086)

client.switch_database('smartgridai')

q = "select * from datasets"

result = client.query(q)

print(result["datasets"])

#print( result['smartmeter'].info() )

#df = pd.DataFrame(result)
#print(df)

#data = pd.read_csv("2019-ETI-EMON-V01-695FA5-1640EF.txt", index_col='Timestamp')
#print(data['consumption_kw'])
#client.write_points(data, "test")

