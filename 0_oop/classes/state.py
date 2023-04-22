class State:
    # state is player dependent
    def __init__(self, player, game):
        self.player = player
        self.player_hand = player.hand
        self.discard_pile = game.discard_pile
        self.draw_pile = game.draw_pile
        self.current_player = game.current_player
        self.players = game.players
