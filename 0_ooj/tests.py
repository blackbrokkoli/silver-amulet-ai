import unittest
from classes.silveramulet import SilverAmulet
from classes.card import Card
from classes.player import Player
from classes.choice import Choice


class TestSilverAmulet(unittest.TestCase):
    def test_create_game_object(self):
        game = SilverAmulet()
        game.generate_deck()
        game.setup()
        self.assertEqual(len(game.draw_pile), 40)

    def test_peek_at_hand_cards(self):
        game = SilverAmulet()
        game.generate_deck()
        game.setup()
        
        game.peek_at_hand_cards(game.players[0], 1)
        # TODO: find a way to automate choices for testing

unittest.main()
