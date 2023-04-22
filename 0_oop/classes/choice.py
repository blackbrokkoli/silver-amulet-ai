import easygui


class Choice:
    def __init__(self, 
                 game, 
                 player, 
                 choice_type, 
                 message, 
                 possible_answers, 
                 show_in_GUI=True, 
                 is_single_choice=True):
        self.player = player
        self.choice_type = choice_type
        self.possible_answers = possible_answers
        self.message = f"{game.get_state_string(player)}\n\n---------------\n\n{player.name}, {message}"
        self.show_in_GUI = show_in_GUI
        self.answer = None
        self.is_single_choice = is_single_choice

    def make_choice(self):
        if self.show_in_GUI:
            if self.is_single_choice:
                print("Possible answers: ", self.possible_answers)
                self.answer = easygui.choicebox(
                    self.message, self.choice_type, self.possible_answers)
            else:
                self.answer = easygui.multchoicebox(
                    self.message, self.choice_type, self.possible_answers)
        return self.answer
    def set_answer(self, answer):
        self.answer = answer
