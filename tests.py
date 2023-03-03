import unittest
from classes.silveramulet import SilverAmulet
from classes.card import Card
from classes.player import Player
from classes.choice import Choice


class TestCreateGameObject(unittest.TestCase):
    def test_create_game_object(self):
        game = SilverAmulet()