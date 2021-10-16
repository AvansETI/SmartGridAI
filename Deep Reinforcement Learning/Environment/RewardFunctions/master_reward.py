from Environment.RewardFunctions.reward_functions import power_reward
from Environment.RewardFunctions.reward_functions import energy_reward
from Environment.RewardFunctions.reward_functions import happiness_reward
from Environment.RewardFunctions.reward_functions import grid_penalty
from Environment.RewardFunctions.reward_functions import overdue_penalty

class MasterReward:
    def __init__(self, a, b, grid_game_over=False, overdue_game_over=False):
        self._grid_game_over = grid_game_over
        self._overdue_game_over = grid_game_over
        self._a = a
        self._b = b

    def calculate(self, state):
        return power_reward(state) + self._a * energy_reward(state) + self._b * happiness_reward(state) \
            + (grid_penalty(state) if self._grid_game_over else 0) \
            + (overdue_penalty(state) if self._overdue_game_over else 0)
