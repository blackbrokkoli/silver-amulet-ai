from ray.tune.registry import register_env
from amulet_env import CardGameEnv

def card_game_creator(_):
    return CardGameEnv()

register_env("CardGame-v0", card_game_creator)
