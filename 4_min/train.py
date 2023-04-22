import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from gym.envs.registration import register

from amulet_env import CardGameEnv

register(id='CustomEnv-v0', entry_point='amulet_env:CardGameEnv')

# Parallel environments
env = make_vec_env("CustomEnv-v0", n_envs=4)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo_amulet")