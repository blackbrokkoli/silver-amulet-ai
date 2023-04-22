import gymnasium as gym
from stable_baselines3 import DQN

def main():
    env = gym.make('CardGame-v0')

    model = DQN.load("dqn_card_game")

    for episode in range(5):
        obs = env.reset()
        done = False
        while not done:
            env.render()
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _ = env.step(action)

        print("Game Over")

if __name__ == "__main__":
    main()
