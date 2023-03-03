class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discard = []
        self.score = 0
        self.amulet = None
        self.number_of_draws = 1

    def __str__(self):
        return self.name

    def play_amulet(self, card):
        self.hand.remove(card)
        self.discard.append(card)
        self.amulet = card
