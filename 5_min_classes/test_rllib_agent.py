import ray
from ray.rllib.agents import ppo
from amulet_env import CardGameEnv

def main():
    ray.init()

    config = ppo.DEFAULT_CONFIG.copy()
    config["framework"] = "torch"
    
    agent = ppo.PPOTrainer(config, env="CardGame-v0")
    
    # Load the latest checkpoint
    checkpoint_path = "path/to/your/checkpoint"
    agent.restore(checkpoint_path)

    env = CardGameEnv()

    for episode in range(5):
        obs = env.reset()
        done = False
        while not done:
            env.render()
            action = agent.compute_action(obs)
            obs, reward, done, _ = env.step(action)

        print("Game Over")

if __name__ == "__main__":
    main()
