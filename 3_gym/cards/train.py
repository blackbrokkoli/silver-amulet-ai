import numpy as np
from simple_card_battle_env import CardBattleEnv
from q_learning_agent import QLearningAgent

num_episodes = 5000

env = CardBattleEnv()
agent = QLearningAgent(env.action_space)

for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        agent.learn(state, action, reward, next_state, done)
        state = next_state

    if (episode + 1) % 100 == 0:
        print(f"Episode {episode + 1}/{num_episodes} completed.")
