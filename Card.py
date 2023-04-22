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
