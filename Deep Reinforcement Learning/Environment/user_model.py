# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# User model
# Simulating the user that uses the flexible and fixed loads.
#
# Future improvements:
# * Implement user interaction, how satisfyed a user is.

import numpy as np
from Environment.appliance_model import ApplianceModel

class UserModel:

    def __init__(self, config):
        # Flexible loads
        self.washing_machine_30 = ApplianceModel("washing_machine_30", { 'data_file': "washing_machine_30.csv" })
        self.washing_machine_60 = ApplianceModel("washing_machine_60", { 'data_file': "washing_machine_60.csv" })
        self.dish_washer        = ApplianceModel("dish_washer",        { 'data_file': "dish_washer.csv"        })

        self.flex_loads = [
            self.washing_machine_30,
            self.washing_machine_60,
            self.dish_washer,
        ]

        # Fixed loads
        self.base_load_w = 240

    def step(self, timestep_s):
        for load in self.flex_loads:
            load.step(timestep_s)
            load.print()

    def print(self):
        print("UserModel")
