import random
import easygui
from .card import Card
from .player import Player
from .choice import Choice
from .state import State


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
        message = f"{self.get_state_string(player)}\{player}, you are about to receive: [ {received_card} ]\nWhat do you want to exchange it with?"
        choices = []
        print("choices: ", choices)
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

        type_of_move = easygui.buttonbox(
            f"\n\n{player.name}, what do you want to do? \n{self.get_state_string(player)}", choices=choices)
        print(f"{player.name} chose {type_of_move}")

        if type_of_move == "Take a card from the deck":
            temporary_cards = []
            for i in range(player.number_of_draws):
                message = f"{self.get_state_string(player)}\n{player}, from where do you want to draw a card?"
                # options are the draw pile (facedown), and every card from the open draw pile
                choices = [f"{self.draw_pile[0].id}: [ Draw pile ▯ ]"]
                print("choices: ", choices)
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
            message = f"{self.get_state_string(player)}\n{player}, which card do you want to take?"
            choices = []
            for card_tuple in temporary_cards:
                card = card_tuple[0]
                choices.append(card.show_card_with_id())
            print("choices: ", choices)
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
            message = f"{self.get_state_string(player)}\n{player}, you drew: [ {drawn_card} ]\nWhat do you want to do with it?\n\nAbility: {drawn_card.ability}"
            choices = ["Exchange with hand cards", "Discard it"]
            # if the type_ability of the card is "drawn", add "Use it and discard"
            if drawn_card.type_ability == "drawn":
                choices.append("Use it and discard")
            print("choices: ", choices)
            action = easygui.buttonbox(message, choices=choices)

            if action == "Exchange with hand cards":
                print(f"Player {player.name} chose to exchange {drawn_card} with hand cards.")
                self.exchange_card_with_hand_cards(player, drawn_card)
            elif action == "Use it and discard":
                print(f"Player {player.name} chose to use {drawn_card} and discard it.")
                self.execute_ability(drawn_card, player)
                self.discard_pile.append(drawn_card)
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
            possible_answers = [str(x+1) for x in [*range(len(player.hand))]]
            choice = Choice(
                self,
                player,
                "peek-at-own-card",
                "which card do you want to peek at?",
                possible_answers,
                True
            )
            choice.make_choice()
            peek_card = choice.answer
            player.hand[int(peek_card) - 1].is_known_to_owner = True

    def play(self):
        # allow each player in turn to peek at two cards on his hand
        for player in self.players:
            self.peek_at_hand_cards(player, 2)

        # the actual rounds of game play
        while self.number_of_remaining_rounds > 0:
            self.number_of_remaining_rounds -= 1
            self.play_round()
        
        self.determine_winner()

    def add_card_to_open_draw_pile(self):
        card = self.draw_pile[0]
        self.open_draw_pile.append(card)
        self.draw_pile.remove(card)

    def turn_card_faceup(self, card_idx, player):
        card = player.hand[card_idx]
        card.is_faceup = True
        if card.type_ability == "faceup":
            self.execute_ability(card, player)

    def card_not_faceup(self, card, player):
        if card.type_ability == "faceup":
            self.undo_faceup_ability(card, player)
        card.is_faceup = False

    def choose_any_players_card(self, any_player, message):
        choices = [str(x+1) for x in [*range(len(any_player.hand))]]
        print("choices: ", choices)
        chosen_card_index = easygui.buttonbox(
            f"\n\n{any_player.name}, {message}" , choices=choices)
        print(f"{any_player.name} chose {chosen_card}")
        return chosen_card_index-1
    
    def choose_a_player(self, player, message, isPlayerIncluded=True):
        if isPlayerIncluded:
            choices = [any_player.name for any_player in self.players]
        else:
            other_players = []
            for game_player in self.players:
                if game_player != player:
                    other_players.append(game_player)               
            choices = [player.name for player in other_players]
            
        print("choices: ", choices)
        chosen_player = easygui.buttonbox(
            f"\n\n{player.name}, {message}", choices=choices)
        print(f"{player.name} chose {chosen_player}")
        
        # find player object by name
        chosen_player_object = None 
        for game_player in self.players:
            if game_player.name == chosen_player:
                chosen_player_object = game_player
                break
        return chosen_player_object

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
                message = "which card do you want to protect?"
                protect_card_idx = self.choose_any_players_card(player, message)
                player.hand[int(protect_card_idx)].is_protected = True
            case 4:
                # When faceup: draw 1 extra card from the deck
                player.number_of_draws += 1
            case 5:
                # Turn 1 of your cards faceup
                message = "which of your cards do you want to turn?"
                card_to_flip_idx = self.choose_any_players_card(player, message)
                self.turn_card_faceup(card_to_flip_idx, player)
            case 6:
                # Turn any 1 card faceup
                choices = [player.name for player in self.players]
                print("choices: ", choices)
                chosen_player = easygui.buttonbox(
                    f"\n\n{player.name}, whose card do you want to turn?", choices=choices)
                print(f"{player.name} chose {chosen_player}")
                
                # find player object by name
                chosen_player_object = None 
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break
                
                message = "which of their cards do you want to turn?"
                card_to_flip = self.choose_any_players_card(chosen_player_object, message)
                self.turn_card_faceup(card_to_flip, chosen_player_object)
            case 7:
                # View up to 2 of your cards
                self.peek_at_hand_cards(player, 2)
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
                
                message = "which of their cards do you want to turn?"
                card_to_flip_idx = self.choose_any_players_card(player, message)
                self.turn_card_faceup(card_to_flip_idx)
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
                drawn_card = self.draw_pile[0]
                self.draw_pile.remove(drawn_card)
                message = f"{self.get_state_string(player)}\n{player}, you drew: [ {drawn_card} ]\nWhose card do you want to exchange with it?"

                other_players = []
                for game_player in self.players:
                    if game_player != player:
                        other_players.append(game_player)
                        
                choices = [player.name for player in other_players]
                print("choices: ", choices)
                chosen_player = easygui.buttonbox(message, choices=choices)
                print(f"{player.name} chose {chosen_player.name}")

                choices = [str(x+1) for x in [*range(len(player.hand))]]
                card_to_flip = easygui.buttonbox(
                    f"\n\n{player.name}, which of your cards do you want to turn?", choices=choices)
                print(f"{player.name} chose {card_to_flip}")
                self.turn_card_faceup(card_to_flip, player)

                # find player object by name
                chosen_player_object = None 
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break

                choices = [str(x+1) for x in [*range(len(chosen_player_object.hand))]]
                print("choices: ", choices)
                card_to_exchange = easygui.buttonbox(
                    f"\n\n{player.name}, which of their cards do you want to exchange?", choices=choices)
                print(f"{player.name} chose {card_to_exchange}")
                
                self.discard_pile.append(chosen_player_object.hand[card_to_exchange-1])
                chosen_player_object.hand[card_to_exchange-1] = drawn_card

            case 12:
                # Steal 1 opponent's card and give them 1 of your cards. View your new card.
                choices = [str(x+1) for x in [*range(len(player.hand))]]
                print("choices: ", choices)
                your_card_to_exchange = easygui.buttonbox(
                    f"\n\n{player.name}, which of your cards do you want to exchange?", choices=choices)
                print(f"{player.name} chose {your_card_to_exchange}")

                other_players = []
                for game_player in self.players:
                    if game_player != player:
                        other_players.append(game_player)
              
                choices = [player.name for player in other_players]
                print("choices: ", choices)
                chosen_player = easygui.buttonbox(
                    f"\n\n{player.name}, whose card do you want to steal?", choices=choices)
                print(f"{player.name} chose {chosen_player.name}")

                # find player object by name
                chosen_player_object = None 
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break

                choices = [str(x+1) for x in [*range(len(chosen_player_object.hand))]]
                print("choices: ", choices)
                card_to_steal = easygui.buttonbox(
                    f"\n\n{player.name}, which of their cards do you want to steal?", choices=choices)
                print(f"{player.name} chose {card_to_steal}")

                tmp_chosen_players_card = chosen_player_object.hand[card_to_steal-1]
                chosen_player_object.hand[card_to_steal-1] = player.hand[your_card_to_exchange-1]
                player.hand[your_card_to_exchange-1] = tmp_chosen_players_card

                player.peek_at_hand_cards(self, player, 1)

                
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
