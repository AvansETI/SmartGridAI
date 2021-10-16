# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# 10-12-2019 - version 0.2
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Appliance model
# Simulation of a generic appliance. It can be used to implement different kinds of appliances.
# This appliance model implement a on/off type of appliance. When it put on, it will stop until it
# is finished. The data of the file looks like:
# timestamp;actual_w;actual_calc_wh;actual_wh
# 0;348;0;0
# 20;354;1.933333333;1.999999999
#
# Future improvements:
# * Implement a planning, when the user want to plan it in.
#   a timer when the appliance should be ready

import os
import numpy as np
from Environment.time_serie_reader import TimeSerieReader

class ApplianceModel:

    def __init__(self, name, config):
        self.name        = name
        self.data_file   = config.get('data_file', "data\\test-data.csv")
        self.data_file   = os.path.dirname(os.path.realpath(__file__)) + "\\data\\" + self.data_file
        self.tsr         = TimeSerieReader( self.data_file )

        print("Appliance file: '" + self.data_file)

        self._reset()        

    def step(self, timestep_s): # Check here wheter the machine is off.
        if ( not self.running ):
            return 0 # Return 0 Wh

        self.timestamp = self.timestamp + timestep_s

        data         = self.tsr.interpolate(self.timestamp)  # Get the data at the timestamp!
        delta_wh     = data['actual_calc_wh'] - self.prev_wh # Calculate the delta wh
        self.prev_wh = data['actual_calc_wh']

        self.actual_wh = data['actual_calc_wh']
        self.actual_w  = data['actual_w']

        if ( self.tsr.reached_end ): # The data file is fully read!
            self._reset()

        return delta_wh

    # This method starts the washing machine
    def start(self):
        if ( not self.running ):
            self.running   = True
            self.step(0) # Perform the first step at timestamp zero!

    def is_running(self):
        return self.running

    # Implement this?!
    def timeleft(self):
        if ( self.running ):
            return self.tsr.get_last_record()['timestamp'] - self.timestamp
        return 0

    # This function returns how much this appliance requires for one run.
    def required_wh(self):
        return self.tsr.get_last_record()['actual_calc_wh']

    # This method is called when the washing machine stopped. # copy of init!
    def _reset(self):
        # State variables
        self.running   = False # When started is given, the machine will be running until is stops!
        self.timestamp = 0     # The timestamp where the process currently is busy with
        self.actual_wh = 0     # The wh value this is currently actual
        self.actual_w  = 0     # The actual power the appliance produces at this timestamp
        self.prev_wh   = 0     # Remember the last prev_w, so we can give the delta wh back between timestamps
        
        self.tsr.start_over()

    def print(self):
        print("Appliance '" + self.name + "' (" + str(self.timestamp) + " / " + str(self.timeleft()) + "):" + str(self.actual_wh) + " Wh, " + str(self.actual_w) + " W")
