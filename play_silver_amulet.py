# implements the card game Silver: Amulet by Teo Alspach
import easygui
import random

class Card:
    instances = []

    def __init__(self, value):
        self.id = Card.generate_unique_id()
        self.value = value
        self.name = ""
        self.ability = ""
        self.type_ability = None
        self.ability_used = False
        self.is_faceup = False
        self.is_known_to_owner = False
        self.owner = None

        self.initialize_card()

        self.__class__.instances.append(self)

    def __str__(self):
        return f"{self.id}: [ {self.value} ]"

    def show_card_to_player(self, player):
        if self.is_faceup or self.is_known_to_owner and player == self.owner:
            return f"{self.id}: [ {self.value} | {self.name} ]"
        else:
            return f"{self.id}: [ ▯ ]"

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
                self.type_ability = "faceup"
                self.ability = "When faceup: If any other 0 is faceup in any village, the round ends instantly."
            case 1:
                self.name = "1 Squire"
                self.type_ability = "faceup"
                self.ability = "When faceup: display 1 card faceup from the deck."
            case 2:
                self.name = "2 Empath"
                self.type_ability = "faceup"
                self.ability = "When faceup: view 1 of your facedown cards on your turn."
            case 3:
                self.name = "3 Bodyguard"
                self.type_ability = "faceup"
                self.ability = "When faceup: protect this and 1 other card from opponents."
            case 4:
                self.name = "4 Rascal"
                self.type_ability = "faceup"
                self.ability = "When faceup: draw 1 extra card from the deck."
            case 5:
                self.name = "5 Exposer"
                self.type_ability = "drawn"
                self.ability = "Turn 1 of your cards faceup."
            case 6:
                self.name = "6 Revealer"
                self.type_ability = "drawn"
                self.ability = "Turn any 1 card faceup."
            case 7:
                self.name = "7 Beholder"
                self.type_ability = "drawn"
                self.ability = "View up to 2 of your cards."
            case 8:
                self.name = "8 Apprentice Seer"
                self.type_ability = "drawn"
                self.ability = "View 1 card of an opponent."
            case 9:
                self.name = "9 Seer"
                self.type_ability = "drawn"
                self.ability = "View any1 card."
            case 10:
                self.name = "10 Master"
                self.type_ability = "drawn"
                self.ability = "Take any 1 card from the discard pile."
            case 11:
                self.name = "11 Witch"
                self.type_ability = "drawn"
                self.ability = "View the top card from the deck nd exchange it into any village."
            case 12:
                self.name = "12 Robber"
                self.type_ability = "drawn"
                self.ability = "Steal 1 opponent's card and give them 1 of your cards. View your new card."
            case 13:
                self.name = "13 Doppelgänger"
                self.type_ability = "discard"
                self.ability = "When discarding: this card matches 1 other card."
            case _:
                print("Card has an unexpected value")


class Ability:
    def __init__(self, name, ability_type):
        self.name = name
        self.ability_type = ability_type

    def __str__(self):
        return self.name

    def execute_ability(self, card, game):
        match self.value:
            case 0:
                pass
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case 8:
                pass
            case 9:
                pass
            case 10:
                pass
            case 11:
                pass
            case 12:
                pass
            case 13:
                pass
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
        self.open_draw_pile = []
        self.number_of_remaining_rounds = 4
        self.vote_is_called = False
        self.open_zeros = 0

        self.generate_deck()
        self.setup()
        self.play()

    def get_state_string(self, current_player=None):
        # print the game state
        state = f"Draw pile ({len(self.draw_pile)} cards): ▯" + "\n"
        state += f"Discard pile ({len(self.discard_pile)} cards): {self.discard_pile[-1]} " + "\n"
       
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
            self.draw_pile.append(Card(0))
            self.draw_pile.append(Card(13))
        for i in range(4):
            for j in range(1, 13):
                self.draw_pile.append(Card(j))

        random.shuffle(self.draw_pile)

    def setup(self):
        # create two players
        self.players.append(Player("Maren"))
        self.players.append(Player("Kolja"))
        print(f"The following players are playing: {self.players}")

        # give each player 5 random cards
        for i in range(5):
            for player in self.players:
                self.give_card(player)

        # move one card from the draw pile to the discard pile
        self.discard_pile.append(self.draw_pile[0])
        self.draw_pile.remove(self.draw_pile[0])


    def give_card(self, player):
        # take first card from draw pile and give it to player
        card = self.draw_pile[0]
        self.draw_pile.remove(card)
        player.hand.append(card)
        player.score = player.score + card.value
        card.owner = player

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

        if type_of_move == "Take a card from the deck":
            drawn_card = self.draw_pile[0]
            self.draw_pile.remove(drawn_card)
            state = self.get_state_string(player)
            message = f"{state}\nYou drew: [ {drawn_card} ]\nWhat do you want to do with it?"
            choices = ["Exchange with hand cards", "Discard it"]
            action = easygui.buttonbox(message, choices=choices)

            if action == "Exchange with hand cards":
                print(f"Player {player.name} chose to exchange {drawn_card} with hand cards.")
                message = f"{state}\nYou drew: [ {drawn_card} ]\nWhat do you want to exchange it with it?"
                choices = []
                for card in player.hand:
                    choices.append(f"{card.show_card_to_player(player)}")
                cards_to_exchange = easygui.multchoicebox(
                    message, choices=choices)
                # check if all chosen cards are either of the same value or the value is 13
                card_values = []
                for card_choice in cards_to_exchange:
                    card_values.append(card_choice.split(":")[1])
                card_values_set = set(card_values)
                if len(card_values_set) == 1 or (13 in card_values_set and len(card_values_set) == 2):
                    # exchange the cards
                    for card_name in cards_to_exchange:
                        card_id = card_name.split(":")[0]
                        # find card object by its id
                        card = None
                        for potential_card in player.hand:
                            if potential_card.id == card_id:
                                card = potential_card
                                break

                        player.hand.remove(card)
                        self.discard_pile.append(card)
                    player.hand.append(drawn_card)
                    drawn_card.owner = player
                    drawn_card.is_known_to_owner = True
                    player.score = player.score + drawn_card.value
                else:
                    print("Illegal move.")
                    # TODO: punish!

            else:
                print(f"Player {player.name} chose to discard {drawn_card}.")
                self.discard_pile.append(drawn_card)
                
        if type_of_move == "Take a card from the discard pile":
            # take the last added card
            drawn_card = self.discard_pile[0]
            # self.discard_pile.remove(drawn_card)
            # message = f"{state}\nYou drew: [ {drawn_card} ]\nWhat do you want to exchange it with it?"
            print(f"Player {player.name} chose to exchange {drawn_card} with hand cards.")
        
        if type_of_move == "Call a vote":
            self.vote_is_called = True
            print(f"Player {player.name} called a vote.")

    def play_round(self):
        for player in self.players:
            self.play_turn(player)

    def peek_at_hand_cards(self, player):
        # create easygui to choose which of the two cards of the five hand cards to turn faceup
            peek_card = easygui.buttonbox(
                f"\n\n{player.name}, at which of your cards do you want to peek at first?", choices=["1", "2", "3", "4", "5"])
            player.hand[int(peek_card) - 1].is_known_to_owner = True

            peek_card = easygui.buttonbox(
                f"\n\n{player.name}, at which of your cards do you want to peek at second?", choices=["1", "2", "3", "4", "5"])
            player.hand[int(peek_card) - 1].is_known_to_owner = True

    def play(self):
        # allow each player in turn to peek at two cards on his hand
        for player in self.players:
            self.peek_at_hand_cards(player)

        # the actual rounds of game play
        while self.number_of_remaining_rounds > 0:
            self.number_of_remaining_rounds -= 1
            self.play_round()

    def add_card_to_open_draw_pile(self):
        card = self.draw_pile[0]
        self.open_draw_pile.append(card)
        self.draw_pile.remove(card)

    def execute_ability(self, card):
        # perform ability depending on value of card
        match card.value:
            case 0:
                self.open_zeros += 1
            case 1:
                self.add_card_to_open_draw_pile()
            case 2:
                for _ in range(2):
                    self.peek_at_hand_cards()
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case 8:
                pass
            case 9:
                pass
            case 10:
                pass
            case 11:
                pass
            case 12:
                pass
            case 13:
                pass
            case _:
                print("Card has an unexpected value")



if __name__ == "__main__":
    # start the game
    game = SilverAmulet()
