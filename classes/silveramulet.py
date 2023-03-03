import random
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

    def run_game(self):
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
        possible_answers = []
       
        for card in player.hand:
            possible_answers.append(f"{card.show_card_to_player(player)}")
        choice = Choice(
            self,
            player,
            "pick-exchange-cards",
            f"you are about to receive: [ {received_card} ]\nWhat do you want to exchange it with?",
            possible_answers,
            True,
            False
        )
        choice.make_choice()
        cards_to_exchange = choice.answer
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
        possible_answers = ["Take a card from the deck",
                   "Take a card from the discard pile"]
        if len(player.hand) <= 4:
            possible_answers.append("Call a vote")

        choice = Choice(
            self,
            player,
            "pick-move",
            "what do you want to do?",
            possible_answers
        )
        choice.make_choice()
        type_of_move = choice.answer

        if type_of_move == "Take a card from the deck":
            temporary_cards = []
            for i in range(player.number_of_draws):
                # options are the draw pile (facedown), and every card from the open draw pile
                possible_answers = [f"{self.draw_pile[0].id}: [ Draw pile ▯ ]"]
                for card in self.open_draw_pile:
                    possible_answers.append(card.show_card_with_id())
                choice = Choice(
                    self,
                    player,
                    "pick-card-pile",
                    "from where do you want to draw a card?",
                    possible_answers
                )
                chosen_pile = choice.make_choice()
                # check if card is from draw pile by string matching
                if "Draw pile" in chosen_pile:
                    card_tuple = (self.draw_pile[0], True)
                else:
                    # find card object by its id within the open draw pile
                    card_id = chosen_pile.split(":")[0]
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
            possible_answers = []
            for card_tuple in temporary_cards:
                card = card_tuple[0]
                possible_answers.append(card.show_card_with_id())
           
            choice = Choice(
                self,
                player,
                "pick-card",
                "which card do you want to take?",
                possible_answers
            )
            chosen_card = choice.make_choice()
            # find card object by its id
            card_id = chosen_card.split(":")[0]
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
            
            possible_answers = ["Exchange with hand cards", "Discard it"]
            # if the type_ability of the card is "drawn", add "Use it and discard"
            if drawn_card.type_ability == "drawn":
                possible_answers.append("Use it and discard")
            
            choice = Choice(
                self,
                player,
                "pick-action",
                f"you drew: [ {drawn_card} ]\nWhat do you want to do with it?\n\nAbility: {drawn_card.ability}",
                possible_answers
            )
            action = choice.make_choice()

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
            player.hand[int(peek_card) - 1].show_card_to_player()

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

    def turn_card_faceup(self, card, player):
        card.is_faceup = True
        if card.type_ability == "faceup":
            self.execute_ability(card, player)

    def card_not_faceup(self, card, player):
        if card.type_ability == "faceup":
            self.undo_faceup_ability(card, player)
        card.is_faceup = False

    def choose_any_players_card(self, player, any_player, message):
        possible_answers = [str(x+1) for x in [*range(len(any_player.hand))]]
       
        choice = Choice(
            self,
            player,
            "choose-any-players-card",
            message,
            possible_answers,
        )
        chosen_card_index = choice.make_choice()
        chosen_card = any_player.hand[int(chosen_card_index)-1]
        print(f"{player.name} chose {chosen_card.name}")
        return chosen_card, chosen_card_index-1
    
    def choose_a_player(self, player, message, is_player_included=True):
        if is_player_included:
            possible_answers = [any_player.name for any_player in self.players]
        else:
            other_players = []
            for game_player in self.players:
                if game_player != player:
                    other_players.append(game_player)               
            possible_answers = [player.name for player in other_players]
            
        choice = Choice(
            self,
            player,
            "choose-a-player",
            message,
            possible_answers,
        )
      
        chosen_player = choice.make_choice()        
        # find player object by name
        chosen_player_object = None 
        for game_player in self.players:
            if game_player.name == chosen_player:
                chosen_player_object = game_player
                break
        return chosen_player_object

    def exchange_any_players_card(self, player, any_player, card_to_exchange_idx, card_to_exchange_with):
        any_player.hand[card_to_exchange_idx] = card_to_exchange_with 
        print(f"{player.name} chose {card_to_exchange} with {card_to_exchange_with}")

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
                card_to_protect, _ = self.choose_any_players_card(player, player, message)
                card_to_protect.is_protected = True
            case 4:
                # When faceup: draw 1 extra card from the deck
                player.number_of_draws += 1
            case 5:
                # Turn 1 of your cards faceup
                message = "which of your cards do you want to turn?"
                card_to_flip, _ = self.choose_any_players_card(player, player, message)
                self.turn_card_faceup(card_to_flip, player)
            case 6:
                # Turn any 1 card faceup
                message = "whose card do you want to turn?"
                chosen_player = self.choose_a_player(player, message)
                
                message = "which of their cards do you want to turn?"
                card_to_flip, _ = self.choose_any_players_card(player, chosen_player, message)
                self.turn_card_faceup(card_to_flip, player)
            case 7:
                # View up to 2 of your cards
                self.peek_at_hand_cards(player, 2)
            case 8:
                # View 1 card of an opponent
                message = "whose enemy card do you want to turn?"
                chosen_player = self.choose_a_player(self, player, message, is_player_included=False)
                
                message = "which of their cards do you want to turn?"
                card_to_flip, _ = self.choose_any_players_card(player, message)
                self.turn_card_faceup(card_to_flip, player)
            case 9:
                # View any 1 card
                possible_answers = [str(x+1) for x in [*range(len(self.players))]]
                choice = Choice(
                    self,
                    player,
                    "choose-a-player",
                    "whose card do you want to view?",
                    possible_answers,
                )
                chosen_player = choice.make_choice()
                # find player object by name
                chosen_player_object = None
                for game_player in self.players:
                    if game_player.name == chosen_player:
                        chosen_player_object = game_player
                        break
                    # TODO: finish
            case 10:
                # Take any 1 card from the discard pile
                possible_answers = [card.show_card_with_id() for card in self.discard_pile]
                choice = Choice(
                    self,
                    player,
                    "choose-a-card",
                    "which card do you want to take from the discard pile?",
                    possible_answers,
                )
                chosen_card = choice.make_choice()
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
                chosen_player = self.choose_a_player(player, is_player_included=False)

                message = "which of their cards do you want to exchange?"
                card_to_exchange, card_to_exchange_idx = self.choose_any_players_card(player, chosen_player, message)
                self.turn_card_faceup(card_to_exchange, player)
                
                self.discard_pile.append(card_to_exchange)

                self.exchange_any_players_card(self, player, chosen_player, card_to_exchange_idx, drawn_card)

            case 12:
                # Steal 1 opponent's card and give them 1 of your cards. View your new card.
                message = "which of your cards do you want to exchange?"
                your_card_to_exchange, your_card_to_exchange_idx = self.choose_any_players_card(player, chosen_player, message)

                message = "whose card do you want to turn?"
                chosen_player = self.choose_a_player(player, message)

                message = "which of their cards do you want to steal?"
                card_to_steal, card_to_steal_idx = self.choose_any_players_card(player, chosen_player, message)

                self.exchange_any_players_card(player, chosen_player, card_to_steal_idx, your_card_to_exchange)
                
                chosen_player_object.hand[card_to_steal-1] = your_card_to_exchange
                player.hand[your_card_to_exchange_idx-1] = card_to_steal
                player.hand[your_card_to_exchange_idx-1].show_card_to_player()
                

                
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
        print(f"The winner is {winner.name} with a score of {winner.score}!\n\n{players_and_scores}")
