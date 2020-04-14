# NPC
from character import Character

class NPC(Character):

    def __init__(self, name="", location=None):
        super(NPC, self).__init__(name, location)
        self.actions = {}

    # Returns a list of special commands associated with this character
    def get_commands(self):
        return self.actions.keys()

    # Add actions associated with this person
    def add_action(self, command_text, function, arguments, preconditions=[]):
        self.actions[command_text] = (function, arguments, preconditions)
    
    # Perform a special action associated with this person
    def do_action(self, command_text, game_state):
        if command_text in self.actions:
            function, arguments, preconditions = self.actions[command_text]
            all_conditions_met = True
            for condition in preconditions:
                status = game_state.is_condition_satisfied(condition)
                if not status[0]:
                    all_conditions_met = False
                    print(status[1])
            if all_conditions_met:
                result = function(arguments)
                return result
        else:
            print('Cannot do the action. Try again.')
            return False