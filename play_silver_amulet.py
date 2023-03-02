# implements the card game Silver: Amulet by Teo Alspach
import easygui
import random


class Ability:
    def __init__(self, name, ability_type):
        self.name = name
        self.ability_type = ability_type

    def __str__(self):
        return self.name


class Card:
    instances = []

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
            
    def assign_ability_to_card(self):
        print("FU")
        match self.value:
            case 0:
                self.ability = ""
        


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


class State:
    # state is player dependent
    def __init__(self, player, game):
        self.player = player
        self.player_hand = player.hand
        self.discard_pile = game.discard_pile
        self.draw_pile = game.draw_pile
        self.current_player = game.current_player
        self.players = game.players


class Choice:
    def __init__(self, player, choice_type, possible_answers):
        self.player = player
        self.choice_type = choice_type
        self.possible_answers = possible_answers


class SilverAmulet:
    def __init__(self):
        self.players = []
        self.discard_pile = []
        self.draw_pile = []
        self.number_of_remaining_rounds = 4
        self.vote_is_called = False

        self.generate_deck()
        self.setup()
        self.play()

    def print_state(self):
        # print the game state
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

    def play_turn(self, player):
        # ask the player whose turn it is to choose:
        # Take a card from the deck, take a card from the discard pile, or call a vote
        # the third option is only available if the player has 4 cards or less on his hand
        choices = ["Take a card from the deck", "Take a card from the discard pile"]
        if len(player.hand) <= 4:
            choices.append("Call a vote")
        type_of_move = easygui.buttonbox(f"{player.name}, what do you want to do?", choices=choices)
        print(f"{player.name} chose {type_of_move}")

    def play_round(self):
        for player in self.players:
            self.play_turn(player)
        


    def play(self):
        while self.number_of_remaining_rounds > 0:
            self.number_of_remaining_rounds -= 1
            self.play_round()


if __name__ == "__main__":
    # start the game
    game = SilverAmulet()
