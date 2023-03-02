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

    def __init__(self, value):
        self.id = Card.generate_unique_id()
        self.name = name
        self.value = value
        self.ability = ability
        self.ability_used = False
        self.is_faceup = False
        self.is_known_to_owner = False

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

    def initialize_card(self):
        match self.value:
            case 0:
                self.name = "0 Villager"
                self.ability = "When faceup: If any other 0 is faceup in any village, the round ends instantly."
            case 1:
                self.name = "1 Squire"
                self.ability = "When faceup: display 1 card faceup from the deck."
            case 2:
                self.name = "2 Empath"
                self.ability = "When faceup: view 1 of your facedown cards on your turn."
            case 3:
                self.name = "3 Bodyguard"
                self.ability = "When faceup: protect this and 1 other card from opponents."
            case 4:
                self.name = "4 Rascal"
                self.ability = "When faceup: draw 1 extra card from the deck."
            case 5:
                self.name = "5 Exposer"
                self.ability = "Turn 1 of your cards faceup."
            case 6:
                self.name = "6 Revealer"
                self.ability = "Turn any 1 card faceup."
            case 7:
                self.name = "7 Beholder"
                self.ability = "View up to 2 of your cards."
            case 8:
                self.name = "8 Apprentice Seer"
                self.ability = "View 1 card of an opponent."
            case 9:
                self.name = "9 Seer"
                self.ability = "View any1 card."
            case 10:
                self.name = "10 Master"
                self.ability = "Take any 1 card from the discard pile."
            case 11:
                self.name = "11 Witch"
                self.ability = "View the top card from the deck nd exchange it into any village."
            case 12:
                self.name = "12 Robber"
                self.ability = "Steal 1 opponent's card and give them 1 of your cards. View your new card."
            case 13:
                self.name = "13 Doppelgänger"
                self.ability = "When discarding: this card matches 1 other card."
            case _:
                print("Card has an unexpected value")


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

    def get_state_string(self, current_player=None):
        # print the game state
        state = f"Draw pile ({len(self.draw_pile)} cards): ▯" + "\n"
        state += f"Discard pile ({len(self.discard_pile)} cards)" + "\n"
        # print each card in the discard pile
        for card in self.discard_pile:
            state += f" {card} "

        for player in self.players:
            state += f"\n\n{player.name}'s hand: \n"

            for card in player.hand:
                # only print card if faceup, otherwise print 'X'
                if card.is_faceup or (player == current_player and card.is_known_to_owner):
                    state += f" {card} "
                else:
                    state += " ▯ "
            state += f"\nScore: {player.score}"
            if player.amulet is not None:
                state += f"\nAmulet: {player.amulet}"

        return state + "\n" + "\n"

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

        print(f"The following players are playing: {self.players}")

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
        choices = ["Take a card from the deck",
                   "Take a card from the discard pile"]
        if len(player.hand) <= 4:
            choices.append("Call a vote")

        state = self.get_state_string(player)
        type_of_move = easygui.buttonbox(
            f"\n\n{player.name}, what do you want to do? \n{state}", choices=choices)
        print(f"{player.name} chose {type_of_move}")

    def play_round(self):
        for player in self.players:
            self.play_turn(player)

    def play(self):
        # allow each player in turn to peek at two cards on his hand
        for player in self.players:
            # create easygui to choose which of the two cards of the five hand cards to turn faceup
            peek_card = easygui.buttonbox(
                f"\n\n{player.name}, at which of your cards do you want to peek at first?", choices=["1", "2", "3", "4", "5"])
            player.hand[int(peek_card) - 1].is_known_to_owner = True

            peek_card = easygui.buttonbox(
                f"\n\n{player.name}, at which of your cards do you want to peek at second?", choices=["1", "2", "3", "4", "5"])
            player.hand[int(peek_card) - 1].is_known_to_owner = True

        while self.number_of_remaining_rounds > 0:
            self.number_of_remaining_rounds -= 1
            self.play_round()


if __name__ == "__main__":
    # start the game
    game = SilverAmulet()
