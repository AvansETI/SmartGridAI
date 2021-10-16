# OpenAI Smart Grid environment
# Minor AI - Project: Does a Smart Grid becomes smarter with AI?
# 
# 06-11-2019 - version 0.1
# Maurice Snoeren <mac.snoeren@avans.nl
#
# Testing the OpenAI environment
import gym

from smartgrid_env import SmartgridEnv

env = SmartgridEnv()

env.reset()

for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()
