from Environment.RewardFunctions.reward_functions import power_reward
from Environment.RewardFunctions.reward_functions import energy_reward
from Environment.RewardFunctions.reward_functions import grid_penalty

class EnergyReward:
    def __init__(self, a, grid_game_over=False):
        self._grid_game_over = grid_game_over
        self._a = a
    
    def calculate(self, state):
        return power_reward(state) + self._a * energy_reward(state) \
            + (grid_penalty(state) if self._grid_game_over else 0)
