import numpy as np
from datetime import datetime, timedelta

class HelperFunctions:
    
    # Method that accepts a timestamp and returns 0 - 3600*24 for each day
    # So this could be used when you have calculations that are based on one day!
    def get_day_based_timestamp ( timestamp ):
        return timestamp % (3600*24)

    # Returns the day number within the year
    def get_day_of_year ( timestamp ):
        return np.floor(timestamp / (3600*24)) + 1

    # Returns the date based on the year you give
    def get_date ( year_start, timestamp ):
        return datetime(year_start, 1, 1, 0, 0, 0, 0) + timedelta( seconds=timestamp )

    # Returns the timestamp based on year given from a datetime
    def get_timestamp_from_date ( current_time ):
        start_time = datetime(current_time.year, 1, 1, 0, 0, 0)
        return current_time.timestamp() - start_time.timestamp()


