import numpy as np
import random

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.99, exploration_rate=0.1):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def act(self, state):
        state_key = self.state_to_key(state)
        if random.random() < self.exploration_rate:
            return self.action_space.sample()
        else:
            return self.max_q_action(state_key)

    def learn(self, state, action, reward, next_state, done):
        state_key = self.state_to_key(state)
        next_state_key = self.state_to_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_space.n)

        if not done and next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_space.n)

        target = reward + self.discount_factor * np.max(self.q_table[next_state_key]) if not done else reward
        self.q_table[state_key][action] += self.learning_rate * (target - self.q_table[state_key][action])

    def state_to_key(self, state):
        return tuple(state.flatten().tolist())

    def max_q_action(self, state_key):
        return np.argmax(self.q_table[state_key]) if state_key in self.q_table else self.action_space.sample()
