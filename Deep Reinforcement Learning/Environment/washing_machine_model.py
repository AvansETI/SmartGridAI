# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Washing maschine model
# Simulation of a washing model. The user can load the washing model and give a final time that the washing machine should
# be ready. Based on the generated data the output will be generated.
#
# Future improvements:
# * A schedule by the user when the washing machine should finish.
# * The AI is able start the washing machine.
# * Add time that is left of the machine
# * Add different washing programs

import os
import numpy as np
from time_serie_reader import TimeSerieReader

class WashingMachineModel:

    def __init__(self, config):
        self.program   = config.get('program', 0)
        
        self.file_program = [ file = os.path.dirname(os.path.realpath(__file__)) + "\\data\\test-data.csv" ]
        


        # The data file looks like:
        #  timestamp;actual_w;calc_wh
        #  0;340;0
        #  20;357;1.889
        self.data_file = config.get('data_file', 'data/washing_machine_30_degrees_celsius_program.csv') # TDOD: Read a data file!
        self.fh        = open(self.data_file, 'r', encoding='utf-8-sig')

        self.file_header = self.fh.readline().rstrip().split(";")

        # State variables
        self.running          = False # When started is given, the machine will be running until is stops!
        self.timestamp_actual = []     # The timestamp where the process currently is busy with
        self.power_wh_actual  = []     # The wh value this is currently actual

    # The methode reads the next line in the file and returns the hash. The data is stored in the
    # self.data variable as well. When the file is empty, the self._reset() is called!
    def _read_next_data(self):
        if ( self.running ):
            line = self.fh.readline()

            if ( line ):
                data = line.rstrip().split(";")
                self.data = {}
                for i in range(len(self.file_header)):
                    self.data[self.file_header[i]] = data[i]
                return self.data

            else:
                self._reset()
                return False

    def step(self, timestep_s):
        data               = self._read_next_data() # This method changes the state of self.running when there is no data!
        power_wh_increased = 0

        while ( self.running and int(data['timestamp']) <= (self.timestamp_actual + timestep_s) ):
            print(data)
            power_wh_increased = float(data['calc_wh']) - self.power_wh_actual
            data = self._read_next_data()

        if( self.running ) :
            self.power_wh_actual  = float(data['calc_wh'])
            self.timestamp_actual = self.timestamp_actual + timestep_s 

        return power_wh_increased

    # This method starts the washing machine
    def start(self):
        if ( not self.running ):
            self.running          = True
            self.timestamp_actual = 0

    # This method is called when the washing machine stopped.
    def _reset(self):
        self.fh.close
        self.fh               = open(self.data_file, 'r', encoding='utf-8-sig')
        self.running          = False
        self.timestamp_actual = 0
        self.power_wh_actual  = 0

    def print(self):
        print("Washing machine: " + str(self.power_wh_actual))
