# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 07-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Battery model
# This battery model simulates the behavior of a battery with a certain capacity and maximum power charge and discharge rate.
# The efficiency loss during the conversion of the charge and discharge is not taken into account. A set point is used to 
# control the battery output to a certain level. When the capacity is insufficient, the power output will decrease automatically.
# Currently the dynamic behavior of the battery is not taken into account. The model implements a simple straigthforward
# bucket model that can be charges and discharged.
#
# Future improvements:
# * Take the efficiency into account of the battery
# * Implement dynamic behavior of the battery
# * Implementation of a real battery model (check Matlab Simulink)

import numpy as np

class BatteryModel:

    def __init__(self, config):
        # Battery configuration (TESLA Powerwall: https://www.tesla.com/sites/default/files/pdfs/powerwall/Powerwall%202_AC_Datasheet_nl.pdf)
        self.capacity_wh                  = config.get('capacity_wh',               13.5 * 1000)
        self.max_power_charge_w           = config.get('max_power_charge_w',        5 * 1000)
        self.max_power_discharge_w        = config.get('max_power_discharge_w',     self.max_power_charge_w)
        #self.efficiency_ac                = config.get('efficiency_ac',             0.9)

        # State variables
        self.capacity_current_wh   = config.get('capacity_initial_wh', self.capacity_wh / 2.0 )
        self.power_w               = config.get('power_initial_w',     0)
        self.set_point_w           = config.get('set_point_initial_w', 0)

    def step(self, timestep_s, set_point_w):
        self.set_point_w = set_point_w

        #print("timestep: " + str(timestep_s) + ", set_point_w: " + str(set_point_w))
        set_point_w = -set_point_w # A positive setpoint is delivering power to the grid, so therefore minus, so the battery will drain!

        if ( set_point_w > self.max_power_charge_w ):
            set_point_w = self.max_power_charge_w

        if ( set_point_w < -self.max_power_discharge_w ):
            set_point_w = -self.max_power_discharge_w

        set_point_wh    = set_point_w * timestep_s / 3600
        capacity_new_wh = self.capacity_current_wh + set_point_wh 

        if ( capacity_new_wh < 0 ): # Battery is not able to deliver this, recalculate the actual power!
            self.power_w    = self.capacity_current_wh * 3600 / timestep_s
            capacity_new_wh = 0

        elif ( capacity_new_wh > self.capacity_wh ): # Battery is not able to deliver this, recalculate the actual power!
            self.power_w    = -(self.capacity_wh - self.capacity_current_wh) * 3600 / timestep_s
            capacity_new_wh = self.capacity_wh 

        else: # Battery is able to deliver this!
            self.power_w = -3600 * set_point_wh / timestep_s
            
        #print("set_point_wh: " + str(set_point_wh) + ", capacity_new_wh: " + str(capacity_new_wh))
        actual_wh = self.power_w * timestep_s / 3600
        self.capacity_current_wh = capacity_new_wh

        return actual_wh

    def print(self):
        print("Battery: " + str(self.power_w) + " W (" + str(self.capacity_current_wh) + "Wh) - Setpoint: " + str(self.set_point_w))
