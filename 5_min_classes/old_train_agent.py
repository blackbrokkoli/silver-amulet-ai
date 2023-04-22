import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from amulet_env import CardGameEnv

def main():
    env = gym.make('CardGame-v0')
    vec_env = DummyVecEnv([lambda: env])
    
    model = DQN('MlpPolicy', vec_env, verbose=1)
    model.learn(total_timesteps=50000)

    model.save("dqn_card_game")

if __name__ == "__main__":
    main()
