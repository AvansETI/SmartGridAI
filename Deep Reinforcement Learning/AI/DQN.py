import random
import gym
import numpy as np
import tensorflow as tf
import sys
import os
import wandb

from collections import deque
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.optimizers import Adam
from space_wrappers.action_wrappers import DiscretizedActionWrapper
from wandb.keras import WandbCallback
from Environment.smartgrid_test_env import SmartgridTestEnv
from Environment.RewardFunctions.simple_reward import SimpleReward

ENV_NAME = 'smartgrid_test_env'

# Number of CPU cores
NUM_PARALLEL_EXEC_UNITS = 4

#Hyperparameters
GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = 100000
BATCH_SIZE = 20

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995

DISCRETIZATION_FACTOR = 100
MAX_CONSUMPTION_PLS = 200

# CPU config
config = tf.ConfigProto(intra_op_parallelism_threads=NUM_PARALLEL_EXEC_UNITS, inter_op_parallelism_threads=2,
                       allow_soft_placement=True, device_count={'CPU': NUM_PARALLEL_EXEC_UNITS})
session = tf.Session(config=config)
K.set_session(session)
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["KMP_BLOCKTIME"] = "30"
os.environ["KMP_SETTINGS"] = "1"
os.environ["KMP_AFFINITY"] = "granularity=fine,verbose,compact,1,0"

class DQNSolver:
    def __init__(self, observation_space_size, action_space_size):
        wandb.init(project="smartgridai")
        
        self.exploration_rate = EXPLORATION_MAX

        self.action_space_size = action_space_size
        self.observation_space_size = observation_space_size
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(24, input_shape=(6,), activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(self.action_space_size, activation="linear"))
        self.model.compile(loss="mse", optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space_size)
        q_values = self.model.predict(np.reshape(state, [-1, self.observation_space_size]))
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + GAMMA * np.amax(self.model.predict(np.reshape(state_next, [-1, self.observation_space_size]))[0]))
            q_values = self.model.predict(np.reshape(state, [-1, self.observation_space_size]))
            q_values[0][action] = q_update
            self.model.fit(np.reshape(state, [-1, self.observation_space_size]), q_values, verbose=0, callbacks=[WandbCallback(log_batch_frequency=BATCH_SIZE)]) #, callbacks=[WandbCallback()]
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)
        
def normalize(state, prev_state):
    """
        0   Grid [Wh]                       SolarEnergyMax + ConsumptionPowerMax (500 + 1000 = 1500, Grid+500/1500)
        1   Solar Enery [Wh]                SolarEnergyMax (solar_energy / env.solar_panel.max_power) (SolarEnergy / SolarEnergyMax)
        2   Battery Energy [Wh]             -max = 0;   0 = 0.5;    max = 1 
        3   Battery Current Capacity [Wh]   (CurrentCapacity / MaxCapacity)
        4   Consumption power [W]           Consumption Power / Max_Consumption_Power
        5   Time [s] 1/1 - 31/12            time / max_time
    """
    
    dgrid = state[0] - prev_state[0]
    dsol  = state[1] - prev_state[1]
    dbatt = state[2] - prev_state[2]
    dcons = state[4] - prev_state[4]
    dtime = state[5] - prev_state[5]
    if (dtime == 0): dtime = 1
    dbatt_min = -env.battery.max_power_charge_w / 3600 * dtime
    dbatt_max = env.battery.max_power_discharge_w / 3600 * dtime
    dsol_max = (1500 / 3600) * dtime
    state_norm = [0] * len(state)
    state_norm[0] = (dgrid - (-dsol_max + dbatt_min)) / (MAX_CONSUMPTION_PLS + dbatt_max - (-dsol_max + dbatt_min))
    state_norm[1] = dsol / dsol_max
    state_norm[2] = (dbatt - dbatt_min) / (dbatt_max - dbatt_min)
    state_norm[3] = state[3] / env.battery.capacity_wh
    state_norm[4] = dcons / MAX_CONSUMPTION_PLS
    state_norm[5] = state[5] / 31622400

    
    #wandb.log({
    #    'NormieGrid': state_norm[0],
    #    'NormieSol': state_norm[1],
    #    'NormBattEnergy': state_norm[2],
    #    'NormieBattCap': state_norm[3],
    #    'NormieConsumption': state_norm[4],
    #    'NormieTime': state_norm[5],  
    #}, commit=False)

    return state_norm

if __name__ == "__main__":
    global env
    env = SmartgridTestEnv()
    env.set_reward_function(SimpleReward())
    env = DiscretizedActionWrapper(env, DISCRETIZATION_FACTOR)
    observation_space = env.observation_space
    action_space = env.action_space
    dqn_solver = DQNSolver(observation_space.shape[0], action_space.n)
    episode = 0
    while True:
        episode += 1
        state = env.reset()
        state_norm = normalize(state, state)
        step = 0
        while True:
            step += 1
            action = dqn_solver.act(state_norm)
            state_next, reward, terminal, info = env.step(action)
            reward = reward if not terminal else -reward
            state_next_norm = normalize(state_next, state)
            dqn_solver.remember(state_norm, action, reward, state_next_norm, terminal)
            state = state_next

            wandb.log({
                'Episode': episode,
                'Action': action, 
                'Grid [Wh]' : state[0], 
                'Solar Energy [Wh]': state[1], 
                'Battery Energy [Wh]': state[2],
                'Battery Current Capacity [Wh]': state[3],
                'Consumption power [W]': state[4], 
                'Time [s]': state[5],
                'Reward' : reward 
            })

            if terminal:
                break
            if (step % 144 == 0):
                dqn_solver.experience_replay()
