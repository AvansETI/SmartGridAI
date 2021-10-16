import pytest
import numpy as np

from AI.expert_bot import ExpertBot

@pytest.fixture
def expert_bot():
    return ExpertBot()

@pytest.fixture
def observation():
    return [
        0,      # grid_wh
        50,     # solar_wh
        50,     # bat_wh
        80,     # battery.capacity_current_wh
        100,    # consumption_wh
        1       # timestamp
    ]

def test_calc_action_evenProductionAndConsumption_shouldHaveBatterySetpointZero(expert_bot, observation):
    observation[1] = 100    # solar_wh
    assert expert_bot.calc_action(observation)[0] == 0

def test_calc_action_greaterProductionThanConsumptionAndNotFullyChargedBattery_shouldHaveNegativeBatterySetpoint(expert_bot, observation):
    observation[1] = 150    # solar_wh
    assert expert_bot.calc_action(observation)[0] < 0

def test_calc_action_smallerProductionThanConsumptionAndNotEmptyBattery_shouldHavePositiveBatterySetpoint(expert_bot, observation):
    observation[1] = 50    # solar_wh
    assert expert_bot.calc_action(observation)[0] > 0