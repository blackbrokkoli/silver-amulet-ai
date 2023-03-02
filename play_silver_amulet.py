# implements the card game Silver: Amulet by Teo Alspach

import random

class Ability:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Card:
    instances = []
        
    def generate_unique_id():
        # generate a four letter alphabetical id that no other card has like 'bqjx'
        # this is used to identify cards in the game state
        # get all ids that have already been used
        used_ids = []
        for card in Card.instances:
            used_ids.append(card.id)

        # generate a new id until we find one that is not used
        while True:
            id = ""
            for i in range(4):
                id += random.choice("abcdefghijklmnopqrstuvwxyz")
            if id not in used_ids:
                return id

    def __init__(self, name, value, ability):
        self.id = Card.generate_unique_id()
        self.name = name
        self.value = value
        self.ability = ability
        self.ability_used = False
        self.is_faceup = False
        
        self.__class__.instances.append(self)
        

    def __str__(self):
        return f"{self.id}: {self.value}"


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discard = []
        self.score = 0
        self.amulet = None

    def __str__(self):
        return self.name

    def play(self, card):
        self.hand.remove(card)
        self.discard.append(card)
        self.score += card.value
        if card.ability is not None:
            card.ability_used = True

    def play_amulet(self, card):
        self.hand.remove(card)
        self.discard.append(card)
        self.amulet = card

class SilverAmulet:
    def __init__(self):
        self.players = []
        self.current_player = 0
        self.discard_pile = []
        self.draw_pile = []
        self.generate_deck()
        self.setup()

    def print_state(self):
        # print the game state
        print(f"Current player: {self.players[self.current_player]}")
        print(f"Draw pile: {len(self.draw_pile)} cards")
        print(f"Discard pile: {len(self.discard_pile)} cards")
        # show card on top of discard pile
        if len(self.discard_pile) > 0:
            print(f"Top card: {self.discard_pile[-1]}")
        
        # show each player's hand
        print()
        for player in self.players:
            print(f"{player.name}'s hand:")
            for card in player.hand:
                print(f" - {card}")
            print(f"Score: {player.score}")
            if player.amulet is not None:
                print(f"Amulet: {player.amulet}")
            print()            
    
    def generate_deck(self):
        # generate 2 cards each with value 0 and 13, and 4 cards each for values 1-12
        for i in range(2):
            self.draw_pile.append(Card("0", 0, None))
            self.draw_pile.append(Card("13", 13, None))
        for i in range(4):
            for j in range(1, 13):
                self.draw_pile.append(Card(str(j), j, None))

        random.shuffle(self.draw_pile)

    def setup(self):
        # create two players
        self.players.append(Player("Maren"))
        self.players.append(Player("Kolja"))
        # give each player 5 random cards
        for i in range(5):
            for player in self.players:
                self.give_card(player)
        self.print_state()

    def give_card(self, player):
        # take first card from draw pile and give it to player
        card = self.draw_pile[0]
        self.draw_pile.remove(card)
        player.hand.append(card)
        player.score = player.score + card.value

    def draw_and_act(self, player):
        card = self.draw_pile[0]
        # TO DO: add ability
        print(card)
        print("Wanna exchange? Enter 'y'.")
        input_action = input()

        if input_action == "y":
            self
        else:
            self.draw_pile.remove(card)
            self.discard_pile.append(card)

if __name__ == "__main__":
    # start the game
    game = SilverAmulet()