from Environment.RewardFunctions.reward_functions import power_reward
from Environment.RewardFunctions.reward_functions import grid_penalty

class SimpleReward:
    def __init__(self, grid_game_over=False):
        self._grid_game_over = grid_game_over

    def calculate(self, state):
        return power_reward(state) \
            + (grid_penalty(state) if self._grid_game_over else 0)
