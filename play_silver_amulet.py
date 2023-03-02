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
        self.is_protected = False

        self.initialize_card()

        self.__class__.instances.append(self)

    def __str__(self):
        return f"[ {self.name} {'𓁺' if self.is_faceup else ''} {'🛡' if self.is_protected else ''} ]"
    
    def show_card_with_id(self):
        return f"{self.id}: {self}"

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


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discard = []
        self.score = 0
        self.amulet = None
        # TODO: set back to one
        self.number_of_draws = 4

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
        self.number_of_open_zeros = 0
        self.number_of_open_ones = 0
        self.player_who_called_vote = None

        self.generate_deck()
        self.setup()
        self.play()

    def get_state_string(self, current_player=None):
        # print the game state
        state = f"Draw pile ({len(self.draw_pile)} cards): ▯" 
        # add cards from open draw pile
        for card in self.open_draw_pile:
            state += f" {card} "
        state += "\n"
        state += f"Discard pile ({len(self.discard_pile)} cards):"
        if len(self.discard_pile) > 0:
            state += f"{self.discard_pile[-1]} " + "\n"
       
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
        # move one card from the draw pile to the open draw pile just for fun
        # TODO: undo this
        self.open_draw_pile.append(self.draw_pile[0])
        self.draw_pile.remove(self.draw_pile[0])


    def give_card(self, player):
        # take first card from draw pile and give it to player
        card = self.draw_pile[0]
        self.draw_pile.remove(card)
        player.hand.append(card)
        player.score = player.score + card.value
        card.owner = player

    def exchange_card_with_hand_cards(self, player, received_card):
        state = self.get_state_string(player)
        message = f"{state}\{player}, you are about to receive: [ {received_card} ]\nWhat do you want to exchange it with it?"
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
            index_of_exchanged_card = 0
            for card_name in cards_to_exchange:
                card_id = card_name.split(":")[0]
                # find card object by its id
                card = None
                for i, potential_card in enumerate(player.hand):
                    if potential_card.id == card_id:
                        index_of_exchanged_card = i
                        card = potential_card
                        break

                player.hand.remove(card)
                self.discard_pile.append(card)
            # append the received card to the player's hand to the same position as the last exchanged card
            player.hand.insert(index_of_exchanged_card, received_card)
            received_card.owner = player
            received_card.is_known_to_owner = True
            player.score = player.score + received_card.value
        else:
            print("Illegal move.")
            # TODO: punish!

    def play_turn(self, player):
        if player == self.player_who_called_vote:
            return
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
            temporary_cards = []
            for i in range(player.number_of_draws):
                message = f"{state}\n{player}, from where do you want to draw a card?"
                # options are the draw pile (facedown), and every card from the open draw pile
                choices = [f"{self.draw_pile[0].id}: [ Draw pile ▯ ]"]
                for card in self.open_draw_pile:
                    choices.append(card.show_card_with_id())
                print('choices: ', choices)
                choice = easygui.buttonbox(message, choices=choices)
                # check if card is from draw pile by string matching
                if "Draw pile" in choice:
                    card_tuple = (self.draw_pile[0], True)
                else:
                    # find card object by its id within the open draw pile
                    card_id = choice.split(":")[0]
                    card_object = None
                    for card in self.open_draw_pile:
                        if card.id == card_id:
                            card_object = card
                            break
                    card_tuple = (card_object, False)
                temporary_cards.append(card_tuple)
                # remove the card from either the draw pile or the open draw pile
                if card_tuple[1]:
                    self.draw_pile.remove(card_tuple[0])
                else:
                    self.open_draw_pile.remove(card_tuple[0])

            # ask the player to choose one of the cards
            message = f"{state}\n{player}, which card do you want to take?"
            choices = []
            for card_tuple in temporary_cards:
                card = card_tuple[0]
                choices.append(card.show_card_with_id())
            choice = easygui.buttonbox(message, choices=choices)
            # find card object by its id
            card_id = choice.split(":")[0]
            card_object = None
            for card_tuple in temporary_cards:
                card = card_tuple[0]
                if card.id == card_id:
                    card_object = card
                    temporary_cards.remove(card_tuple)
                    break

            # put the other cards back in the same place in the same order
            for card_tuple in reversed(temporary_cards):
                card = card_tuple[0]
                if card_tuple[1]:
                    self.draw_pile.insert(0, card)
                else:
                    self.open_draw_pile.insert(0, card)
                
            drawn_card = card_object
            state = self.get_state_string(player)
            message = f"{state}\n{player}, you drew: [ {drawn_card} ]\nWhat do you want to do with it?"
            choices = ["Exchange with hand cards", "Discard it"]
            action = easygui.buttonbox(message, choices=choices)

            if action == "Exchange with hand cards":
                print(f"Player {player.name} chose to exchange {drawn_card} with hand cards.")
                self.exchange_card_with_hand_cards(player, drawn_card)

            else:
                print(f"Player {player.name} chose to discard {drawn_card}.")
                self.discard_pile.append(drawn_card)
                
        if type_of_move == "Take a card from the discard pile":
            # take the last added card
            drawn_card = self.discard_pile[0]
            self.discard_pile.remove(drawn_card)
            print(f"Player {player.name} chose to exchange {drawn_card} with hand cards.")
            self.exchange_card_with_hand_cards(player, drawn_card)
        
        if type_of_move == "Call a vote":
            self.vote_is_called = True
            self.player_who_called_vote = player
            print(f"Player {player.name} called a vote.")

    def play_round(self):
        for player in self.players:
            self.play_turn(player)

    def peek_at_hand_cards(self, player, n):
        # create easygui to choose which of the two cards of the five hand cards to turn faceup
        for _ in range(n):
            choices = [str(x+1) for x in [*range(len(player.hand))]]
            peek_card = easygui.buttonbox(
                f"\n\n{player.name}, which card do you want to peek at?", choices = choices)
            player.hand[int(peek_card) - 1].is_known_to_owner = True

    def play(self):
        # allow each player in turn to peek at two cards on his hand
        # TODO: uncomment this after testing
        # for player in self.players:
        #     self.peek_at_hand_cards(player, 2)

        # the actual rounds of game play
        while self.number_of_remaining_rounds > 0:
            self.number_of_remaining_rounds -= 1
            self.play_round()
        
        self.determine_winner()

    def add_card_to_open_draw_pile(self):
        card = self.draw_pile[0]
        self.open_draw_pile.append(card)
        self.draw_pile.remove(card)

    def turn_card_faceup(self, card, player):
        card.is_faceup = True
        if card.type_ability == "faceup":
            self.execute_ability(self, card, player)

    def card_not_faceup(self, card, player):
        if card.type_ability == "faceup":
            self.undo_faceup_ability(self, card, player)
        card.is_faceup = False

    def execute_ability(self, card, player):
        # perform ability depending on value of card
        match card.value:
            case 0:
                # When faceup: if any other 0 is faceup in any village, the round ends instantly
                self.number_of_open_zeros += 1
            case 1:
                # When faceup: display 1 card faceup from the deck
                self.number_of_open_ones += 1
                if len(self.draw_pile) < self.number_of_open_zeros:
                    self.add_card_to_open_draw_pile()
            case 2:
                # When faceup: view 1 of your facedown cards on your turn
                for _ in range(2):
                    self.peek_at_hand_cards()
            case 3:
                # When faceup: protect this and 1 other card from opponents
                choices = [str(x+1) for x in [*range(len(player.hand))]]
                protect_card = easygui.buttonbox(
                    f"\n\n{player.name}, which card do you want to protect?", choices = choices)
                player.hand[int(protect_card) - 1].is_protected = True
            case 4:
                # When faceup: draw 1 extra card from the deck
                player.number_of_draws += 1
            case 5:
                # Turn 1 of your cards faceup
                choices = [str(x+1) for x in [*range(len(player.hand))]]
                card_to_flip = easygui.buttonbox(
                    f"\n\n{player.name}, which of your cards do you want to turn?", choices=choices)
                print(f"{player.name} chose {card_to_flip}")
                self.turn_card_faceup(player.hand[int(card_to_flip)])
            case 6:
                # Turn any 1 card faceup
                choices = [player.name for player in self.players]
                chosen_player = easygui.buttonbox(
                    f"\n\n{player.name}, whose card do you want to turn?", choices=choices)
                print(f"{player.name} chose {chosen_player.name}")
                
                # find player object by name
                chosen_player_object = None 
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break

                choices = [str(x+1) for x in [*range(len(chosen_player_object.hand))]]
                card_to_flip = easygui.buttonbox(
                    f"\n\n{player.name}, which of their cards do you want to turn?", choices=choices)
                print(f"{player.name} chose {card_to_flip}")
                self.turn_card_faceup(chosen_player_object.hand[int(card_to_flip)])
            case 7:
                # View up to 2 of your cards
                self.peek_at_hand_cards(self, player, 2)
            case 8:
                # View 1 card of an opponent
                other_players = []
                for game_player in self.players:
                    if game_player != player:
                        other_players 
                
                choices = [player.name for player in other_players]
                chosen_player = easygui.buttonbox(
                    f"\n\n{player.name}, whose card do you want to turn?", choices=choices)
                print(f"{player.name} chose {chosen_player.name}")

                # find player object by name
                chosen_player_object = None 
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break
            case 9:
                # View any 1 card
                choices = [str(x+1) for x in [*range(len(self.players))]]
                chosen_player = easygui.buttonbox(
                    f"\n\n{player.name}, whose card do you want to see?", choices=choices)
                print(f"{player.name} chose {self.players[chosen_player-1].name}")
            case 10:
                # Take any 1 card from the discard pile
                choices = [card.show_card_with_id() for card in self.discard_pile]
                chosen_card = easygui.buttonbox(
                    f"\n\n{player.name}, which card do you want to take from the discard pile?", choices=choices)
                print(f"{player.name} chose {chosen_card}")
                # get card object by id 
                chosen_card_object = None
                for card in self.discard_pile:
                    if card.id == chosen_card.split(":")[0]:
                        chosen_card_object = card
                        break
                # add card to player's hand
                player.hand.append(chosen_card_object)
                # remove card from discard pile
                self.discard_pile.remove(chosen_card_object)
            case 11:
                # View the top card from the deck and exchange it into any village
                
                message = f"{state}\n{player}, you drew: [ {drawn_card} ]\nWhat do you want to do with it?"
                choices = ["Ok."]
                action = easygui.buttonbox(message, choices=choices)
                pass
            case 12:
                # Steal 1 opponent's card and give them 1 of your cards. View your new card.
                pass
            case 13:
                # When discarding: this card matches 1 other card (already implemented)
                pass
            case _:
                print("Card has an unexpected value")

            
    def undo_faceup_ability(self, player, card):
        match card.value:
            case 0:
                self.number_of_open_zeros -= 1
            case 1:
                self.number_of_open_ones -=1
            case 3:
                player.hand[int(protect_card) - 1].is_protected = False
            case 4:
                player.number_of_draws -= 1

    def determine_winner(self):
        # list all players and score in the UI, just with an ok button
        # player with lowest score wins

        winner = None
        lowest_score = 1000
        for player in self.players:
            if player.score < lowest_score:
                winner = player
                lowest_score = player.score
        
        players_and_scores = [f"{player.name}: {player.score}" for player in self.players].join("\n")
        easygui.msgbox(f"The winner is {winner.name} with a score of {winner.score}!\n\n{players_and_scores}")


if __name__ == "__main__":
    # start the game
    game = SilverAmulet()
