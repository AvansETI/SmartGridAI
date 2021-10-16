# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 18-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# TimeSerieReader
# Helps to read time serie data and interpolate the values from a time serie csv file.
# The object requires a file that looks like:
# The data file looks like:
#  timestamp;actual_w;calc_wh
#  0;340;0
#  20;357;1.889
#
# At least timestamp is needed and the rest needs to be values. Everything will be converted
# to floating point numbers. When the EOF is reached, the file is finished!

import numpy as np

class TimeSerieReader:

    def __init__(self, file):
        self.data_file   = file
        self.fh          = open(self.data_file, 'r', encoding='utf-8-sig')
        self.file_header = self.fh.readline().rstrip().split(";")
        self.depth       = 100

        # State variables
        self.eof              = False
        self.reached_end      = False
        self.data             = [0]*self.depth
        self.pointer_current  = 0
        self.pointer_end      = 0
        self.total_elements   = 0

        self._get_last_file_record() # Get some stats of the file by getting the starting and ending record

        self._read_file_data( self.depth )

    # Returns the last record that is in the file. Private function.
    # Bug in the function!
    def _get_last_file_record(self):
        self.record_first = self._convert_line_to_record(self.fh.readline())
        for line in self.fh:
            pass
        self.record_last = self._convert_line_to_record(line)
        self.start_over() # Start over while we have now a corrupted the file handle

    def get_first_record(self):
        return self.record_first

    def get_last_record(self):
        return self.record_last

    def size(self):
        return self.total_elements

    def add(self, data):
        if self.total_elements == self.depth: # cannot add any elements anymore!
            self.pointer_current = (self.pointer_current + 1) % self.depth
        
        if self.total_elements < self.depth:
            self.total_elements = self.total_elements + 1

        self.data[self.pointer_end] = data
        self.pointer_end = (self.pointer_end + 1) % self.depth

    def get(self, index):
        if ( index < 0 or index > self.depth ):
            raise IndexError('index out of range')

        index_real = (index + self.pointer_current) % self.depth        
        return self.data[index_real]

    def end(self):
        return self.get( self.size() - 1)

    # Search the two data points that is hold by the timestamp
    def interpolate(self, timestamp):
        while ( not self.eof and timestamp > self.end()['timestamp'] ): # Search for the measurements where the timestamp is in.
            self._read_file_data( self.depth - 1) # read the next elements, not all so we can perform index - 1

        if timestamp <= self.end()['timestamp']: # When the searched timestamp is within the data set, we can find the closest elements
            index = 0
            while ( index < self.size() - 1 and timestamp >= self.get(index)['timestamp'] ):
                index = index + 1

            if index - 1 < 0: # When it is the first element, interpolate with the next element, instead of the previous one
                index = index + 1

            d1 = self.get(index-1)
            d2 = self.get(index)
            #print("found index: " + str(index) + ": " + str(self.get(index)))
            #print("d1: " + str(d1))
            #print("d2: " + str(d2))

            data_int = { 'timestamp': timestamp } # Interpolate all the values within the data!
            for h in self.file_header:
                if ( h != 'timestamp' ):
                    a = (d2[h]-d1[h]) / (d2['timestamp'] - d1['timestamp'])
                    b = d1[h] - a * d1['timestamp']
                    data_int[h] = timestamp * a + b

            return data_int

        else: # Not found, return the last element
            self.reached_end = True
            return self.end()

    def _read_file_data(self, total):
        counter = 0
        while ( counter < total ):
            line    = self.fh.readline()
            if ( line ):
                self.add( self._convert_line_to_record(line) )
            else:
                counter = total

            counter = counter + 1
        
        if ( not line ):
            self.eof = True

        return counter

    def _convert_line_to_record(self, line):
        data = {}
        raw  = line.rstrip().split(";")
        for i in range(len(self.file_header)):
            data[self.file_header[i]] = float(raw[i])

        return data

    def read(self, timestep_s):
        return 0

    # This method is called when the washing machine stopped.
    def start_over(self):
        self.fh.seek(0, 0)
        self.eof              = False
        self.reached_end      = False
        self.data             = [0]*self.depth
        self.pointer_current  = 0
        self.pointer_end      = 0
        self.total_elements   = 0

        self.file_header = self.fh.readline().rstrip().split(";")
        self._read_file_data( self.depth )

    def print(self):
        print("TimeSerieReader: Size(" + str(self.size()) + "), Current pointer(" + str(self.pointer_current) + "), End point(" + str(self.pointer_end) + "), EOF(" + str(self.eof) + ")")
        for i in range( self.size() ):
            print(str(i) + ": " + str(self.get(i)['timestamp']))
