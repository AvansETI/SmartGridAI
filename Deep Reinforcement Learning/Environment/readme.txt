Documentation: https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
Add to the environment by:
1. Put it some where in the dir: D:\openai\gym\gym\envs
2. Add an entry to the __init__.py: 
register(
    id='SmartGrid-v0',
    entry_point='gym.envs.classic_control:SmartgridEnv',
    max_episode_steps=31622400,
    reward_threshold=90.0,
)
