import gym
from gym import spaces
import numpy as np
import random

class SimpleGameEnv(gym.Env):
    def __init__(self):
        super(SimpleGameEnv, self).__init__()
        
        self.target_score = 10
        self.num_players = 2

        # Define action space: 0 (roll the dice)
        self.action_space = spaces.Discrete(1)

        # Define observation space: [current_player, player_1_score, player_2_score]
        self.observation_space = spaces.Box(low=0, high=self.target_score, shape=(3,), dtype=np.int32)

        self.reset()

    def step(self, action):
        assert self.action_space.contains(action), f"Invalid action {action}"

        # Roll the dice (1 to 6)
        dice_roll = random.randint(1, 6)

        # Update the current player's score
        self.scores[self.current_player] += dice_roll

        # Check if the game is over
        done = any(score >= self.target_score for score in self.scores)

        # Calculate the reward for the current player
        if done:
            if self.scores[self.current_player] >= self.target_score:
                reward = 1  # Current player won
            else:
                reward = -1  # Current player lost
        else:
            reward = 0  # No reward, continue the game

        # Switch to the other player
        self.current_player = 1 - self.current_player

        return self._get_observation(), reward, done, {}

    def reset(self):
        self.scores = [0, 0]
        self.current_player = 0
        return self._get_observation()

    def render(self, mode="human"):
        print(f"Player 1 score: {self.scores[0]} | Player 2 score: {self.scores[1]} | Current player: {self.current_player + 1}")

    def _get_observation(self):
        return np.array([self.current_player] + self.scores, dtype=np.int32)

if __name__ == "__main__":
    env = SimpleGameEnv()
    env.reset()

    done = False
    while not done:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

    env.render()
    print("Game over!")
