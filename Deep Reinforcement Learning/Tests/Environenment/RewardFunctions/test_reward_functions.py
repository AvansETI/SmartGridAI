import pytest
import numpy as np

import Environment.RewardFunctions.reward_functions as rfunc

class Deadline:
    def __init__(self, time, completed):
        self.time = time
        self.completed = completed

@pytest.fixture
def state():
    return {
        'grid_wh': 100,
        'battery_capacity_current_wh': 50,
        'battery_capacity_wh': 2000,
        'deadlines': [],
        'timestamp': 1574884481
    }

def test_power_reward_noUsage_shouldRewardZero(state):
    state['grid_wh'] = 0
    assert rfunc.power_reward(state) == 0

def test_power_reward_useFromGrid_shouldRewardNegative(state):
    state['grid_wh'] = 100
    assert rfunc.power_reward(state) < 0

def test_power_reward_deliverToGrid_shouldRewardPositive(state):
    state['grid_wh'] = -100
    assert rfunc.power_reward(state) > 0

def test_energy_reward_fullBattery_shouldRewardPositive(state):
    state['battery_capacity_current_wh'] = state['battery_capacity_wh']
    assert rfunc.energy_reward(state) > 0

def test_energy_reward_emptyBattery_shouldRewardZeroOrNegative(state):
    state['battery_capacity_current_wh'] = 0
    assert rfunc.energy_reward(state) <= 0

def test_happiness_reward_completedFutureDeadlines_shouldRewardPositive(state):
    state['deadlines'] = [
        Deadline(1574929800, True)
    ]
    assert rfunc.happiness_reward(state) > 0

def test_happiness_reward_completedPastDeadlines_shouldRewardZero(state):
    state['deadlines'] = [
        Deadline(947344800, True)
    ]
    assert rfunc.happiness_reward(state) == 0

def test_happiness_reward_uncompletedFutureDeadlines_shouldRewardZero(state):
    state['deadlines'] = [
        Deadline(1574929800, False)
    ]
    assert rfunc.happiness_reward(state) == 0

def test_happiness_reward_uncompletedPastDeadlines_shouldRewardZeroOrNegative(state):
    state['deadlines'] = [
        Deadline(947344800, False)
    ]
    assert rfunc.happiness_reward(state) <= 0

def test_grid_penalty_usage_shouldRewardNegInf(state):
    state['grid_wh'] = 1
    assert rfunc.grid_penalty(state) == -np.inf

def test_grid_penalty_noUsage_shouldRewardZero(state):
    state['grid_wh'] = 0
    assert rfunc.grid_penalty(state) == 0

def test_overdue_penalty_anyUncompletePastDeadline_shouldRewardNegInf(state):
    state['deadlines'] = [
        Deadline(1574929800, True),
        Deadline(947344800, True),
        Deadline(947344800, False)
    ]
    assert rfunc.overdue_penalty(state) == -np.inf

def test_overdue_penalty_noUncompletePastDeadline_shouldRewardZero(state):
    state['deadlines'] = [
        Deadline(1574929800, True),
        Deadline(947344800, True),
        Deadline(1574929800, False)
    ]
    assert rfunc.overdue_penalty(state) == 0