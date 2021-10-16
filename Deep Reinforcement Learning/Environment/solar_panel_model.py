# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Solar panel model
# This model simulates solar panels. The current model uses external generated data to be fast.
# Muliple data sources could be used. This preprocessed data is used to be fast.
#
# Future improvements:
# * Implementation of a real solar panel model.
# * Based on weather data calculation of the solar output.

import os
import numpy as np

from Environment.time_serie_reader import TimeSerieReader

class SolarPanelModel:

    def __init__(self, config):
        self.program   = config.get('program', 0)
        self.data_file = [ config.get('data_file', 'data/solar-test-data.csv') ]
        self.tsr       = TimeSerieReader( os.path.dirname(os.path.realpath(__file__)) + "/" + self.data_file[0])

        self.max_power = 500

        # State variables
        self.prev_wh   = 0
        self.prev_ts   = 0
        self.timestamp = 0

    def step(self, timestep_s):
        self.timestamp = ( self.timestamp + timestep_s ) % (3600*24)
        timestamp = self.timestamp

        if self.prev_ts > timestamp :
            self.prev_wh = 0
            self.tsr.start_over()

        data = self.tsr.interpolate(timestamp)
        actual_wh = data['actual_wh'] - self.prev_wh

        self.prev_wh = data['actual_wh']
        self.prev_ts = data['timestamp']
        
        return actual_wh

    def print(self):
        print("Solar panel: " + str(self.timestamp))