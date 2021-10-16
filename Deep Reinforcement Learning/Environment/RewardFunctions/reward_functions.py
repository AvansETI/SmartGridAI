import numpy as np

def power_reward(state):
    reward = -state['grid_wh']
    return reward if reward > 0 else reward*2

def energy_reward(state):
    return state['battery_capacity_current_wh'] / state['battery_capacity_wh']

def happiness_reward(state):
    return sum(deadline.completed and deadline.time > state['timestamp'] for deadline in state['deadlines']) / len(state['deadlines'])

def grid_penalty(state):
    return -np.inf if (state['grid_wh'] > 0) else 0

def overdue_penalty(state):
    return -np.inf if any(not deadline.completed and deadline.time < state['timestamp'] for deadline in state['deadlines']) else 0