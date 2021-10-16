# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 30-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Test version of the smart grid environment

import numpy as np
import gym
from gym import spaces

from Environment.battery_model import BatteryModel
from Environment.solar_panel_model import SolarPanelModel

class SmartgridEnv(gym.Env):
    """
    Description:
        Smart grid environment that simulates a household for one year. This version is a first initial version to test the openai environment model.

    Observation: 
        Type: Box(5)
        Num	Observation                     Min         Max
        0   Grid [Wh]                       0           Inf
        1	Solar Energy [Wh]               0           Inf
        2   Battery Energy [Wh]             -Inf        Inf
        3   Battery Current Capacity [Wh]   0           Inf
        4   Consumption power [W]           0           Inf
        5   Time [s] 1/1 - 31/12            0           31622400 

        NOTE: Consumption is fixed to 240W

    Actions:
        Type: Box(1)
        Num	Action                      Min         Max
        0	Battery Set Point           -cap_W      +cap_W
        
    Reward:
        Reward is the difference of the sum (of each step) of solar power + battery power and consumption.
        Reward = sum(Solar Power) + sum(Battery) - sum(Consumption)
        Reward range -Inf to Inf

    Starting State:
        Observations start at zero.

    Episode Termination:
        After one year.
        Later: When the power grid is used!
    """
    metadata = {'render.modes': ['human']}

    # Constructor that accepts a configuration config variabele to setup the smartgrid environment
    def __init__(self, config):
        # Reward function that can be set
        self.reward_function   = None

        # Configuration of the environment
        self.battery = BatteryModel({})
        self.solar_panel = SolarPanelModel({})

        # State variables
        self.timestep          = 10*60 # 10 minutes per step [s]
        self.timestamp         = 0
        self.grid_wh           = 0
        self.bat_wh            = 0
        self.solar_wh          = 0
        self.consumption_wh    = 0
        
        # OpenAI spaces
        self.action_space      = spaces.Box(np.array([self.battery.max_power_discharge_w]), np.array([self.battery.max_power_charge_w]), dtype=np.float16)
        self.observation_space = spaces.Box(np.array([0, 0, -np.Inf, 0, 0, 0]), np.array([np.Inf, np.Inf, np.Inf, np.Inf, np.Inf, 31622400]), dtype=np.float16)
        self.reward_range      = (-np.Inf, np.Inf)

    def set_reward_function(self, reward_function):
        calculate_method = getattr(reward_function, "calculate", None) # Check whether the reward object has a callable method calculate!
        if callable(calculate_method):
            self.reward_function = reward_function

        else:
            print("Error: reward function should be a object with a method 'calculate'!")

    def step(self, action):
        if ( not self._is_done() ):
            self.timestamp = self.timestamp + self.timestep

            # Tie the actions to real variables!
            set_point_w = action[0]

            self.bat_wh         = self.bat_wh + self.battery.step(self.timestep, set_point_w)
            self.solar_wh       = self.solar_wh + self.solar_panel.step(self.timestep)
            self.consumption_wh = self.consumption_wh + (240 * self.timestep / 3600)
            self.grid_wh        = self.consumption_wh - self.bat_wh - self.solar_wh

            #print("grid_wh: " + str(self.grid_wh))
            #self.battery.print()
            #self.solar_panel.print()
            #print("grid_wh: " + str(self.grid_wh) + ", battery (wh): "+ str(self.bat_wh) + ", solar (wh): " + str(self.solar_wh))

        return self._get_observation(), self._reward(), self._is_done(), self._get_info()

    def _get_info(self):
        return {
            'battery': self.battery,
            'solar_panel': self.solar_panel
        }

    # This method creates the observation matrix from all the models that have been used for the smart grid model
    def _get_observation(self):
        return np.array([ 
            self.grid_wh,
            self.solar_wh,
            self.bat_wh,
            self.battery.capacity_current_wh,
            self.consumption_wh,
            self.timestamp,
        ])

    # This method return true when the environment is done, otherwise false.
    def _is_done(self):
        return self.timestamp >= 31536000 # 24 * 3600 * 365

    # This method creates a state variable that is used by the reward function
    def _get_state(self):
         return { 
            'grid_wh': self.grid_wh,
            'solar_wh': self.solar_wh,
            'battery_wh': self.bat_wh,
            'battery_capacity_current_wh': self.battery.capacity_current_wh,
            'consumption_wh': self.consumption_wh,
            'timestamp': self.timestamp,
         }

    # This method calculates the reward of the environment.
    def _reward(self):
        if ( self.reward_function == None ):
            print("Note: no reward function has been set!")
            return -self.grid_wh # Default reward function

        self.reward_function.calculate( self._get_state() ) # Call the reward function for the real rewards!

    def reset(self):
        self.time = 0
        self.batCurrentPower = 0
        self.solarCurrentPower = 0
        self.consCurrentPower = 0

    def render(self, mode='human', close=False):
        grid = self.batCurrentPower + self.solarCurrentPower - self.consCurrentPower
        print("smartgrid (" + str(self.time) + "): " + str(grid))
