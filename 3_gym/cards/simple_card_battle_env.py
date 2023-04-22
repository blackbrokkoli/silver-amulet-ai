import gym
from gym import spaces
import numpy as np
import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

class CardBattleEnv(gym.Env):
    def __init__(self):
        super(CardBattleEnv, self).__init__()

        self.target_score = 10
        self.num_players = 2
        self.hand_size = 5

        # Define action space: 0-4 (play a card), 5-9 (discard and draw)
        self.action_space = spaces.Discrete(10)

        # Define observation space: [current_player, scores, hands, deck_size]
        max_deck_size = 52 - 2 * self.hand_size
        self.observation_space = spaces.Tuple((
            spaces.Discrete(self.num_players),
            spaces.Box(low=0, high=self.target_score, shape=(self.num_players,), dtype=np.int32),
            spaces.Box(low=1, high=13, shape=(2 * self.hand_size,), dtype=np.int32),
            spaces.Discrete(max_deck_size + 1)
        ))

        self.reset()

    def step(self, action):
        assert self.action_space.contains(action), f"Invalid action {action}"

        if action < 5:
            # Play a card
            card_index = action
            card = self.hands[self.current_player][card_index]
            self.board[self.current_player] = card
            self.hands[self.current_player][card_index] = None

            if all(c is not None for c in self.board):
                # Both players have played a card; resolve the round
                if self.board[0].rank > self.board[1].rank:
                    self.scores[0] += 1
                elif self.board[1].rank > self.board[0].rank:
                    self.scores[1] += 1

                self.board = [None, None]
                self.current_player = 0
            else:
                # Switch to the other player
                self.current_player = 1 - self.current_player
        else:
            # Discard and draw
            if self.deck:
                card_index = action - 5
                self.hands[self.current_player][card_index] = self.deck.pop()

        # Check if the game is over
        done = any(score >= self.target_score for score in self.scores) or not self.deck

        # Calculate the reward for the current player
        if done:
            if self.scores[self.current_player] >= self.target_score:
                reward = 1  # Current player won
            else:
                reward = -1  # Current player lost
        else:
            reward = 0  #
