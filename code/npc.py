# NPC
from character import Character

class NPC(Character):

    def __init__(self, name="", location=None):
        super(NPC, self).__init__(name, location)
        self.actions = {}

    # Add actions associated with this person
    def add_action(self, command_text, function, arguments, preconditions=[]):
        self.actions[command_text] = (function, arguments, preconditions)
    
    # Perform a special action associated with this person
    def do_action(self, command_text, game_state):
        if command_text in self.actions:
            function, arguments, preconditions = self.actions[command_text]
            all_conditions_met = True
            for condition in preconditions:
                if not game_state.is_condition_satisfied(condition):
                    all_conditions_met = False
            if all_conditions_met:
                result = function(arguments)
                return result
        else:
            print('Cannot do the action. Try again.')
            return False