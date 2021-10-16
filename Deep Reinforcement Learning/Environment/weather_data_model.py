# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Weather data model
# This model generates weather data based on existing weather data. It generate also a forecasting of the weather data.
#
# Future improvements:
#

import numpy as np

class WeatherDataModel:

    def __init__(self, config):
        self.program   = config.get('program', 0)

        # The data file looks like:
        # 
        self.data_file = config.get('data_file', 'data/washing_machine.dat') # TDOD: Read a data file!

        # State variables
        self.started        = False # Started is the boolean that shows that the machine is running!
        self.power_w         = 0
        self.total_time_left = 0

    def step(self, timestep_s):
        if ( self.started ):
            self.power_w = 3000
            self.total_time_left = self.total_time_left - timestep_s

            if ( self.total_time_left < 0 ):
                self.total_time_left = 0
                self.started = False

        else:
            self.power_w = 0
            self.total_time_left = 0

    def start(self):
        if ( self.started == False ):
            self.started = True
            self.total_time_left = 60*60*3 # Just for testing!

    def print(self):
        print("Washing machine: " + str(self.power_w) + " (Total time left: " + str(self.total_time_left) + " s)")
