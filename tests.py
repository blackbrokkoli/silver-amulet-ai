import unittest
from .play_silver_amulet import *

class TestCreateGameObject(unittest.TestCase):
    def test_create_game_object(self):
        game = SilverAmulet()