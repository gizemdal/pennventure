# Item
from location import Location
import string

item_id = 0 # unique item id, assigned by creation order

class Item(object):

    def __init__(self, 
                 name, 
                 description, 
                 collectable=True, 
                 examine_text="", 
                 location=None):
        global item_id
        # The name of the item
        self.name = name.lower()
        # The default description of the item.
        self.description = description
        # Indicates whether a player can get the item and put it in their inventory.
        self.collectable = collectable
        # The detailed description of the player examines the object.
        self.examine = examine_text
        # The location in the game where the item starts.
        self.location = location
        if self.location:
            self.location.add_item(self.name, self)
        self.actions = {}
        self.id = item_id
        item_id += 1
    
    def __eq__(self, other):
        return self.id == other.id
    
    # Change the location of the item
    def change_location(self, new_location):
        if self in self.location.items[self.name]:
            self.location.remove_item(self)
        self.location = new_location
        if self.location:
            self.location.add_item(self.name, self)

    # Returns a list of special commands associated with this object
    def get_commands(self):
        return self.actions.keys()
    
    # Add a special action associated with this item
    def add_action(self, command_text, function, arguments, preconditions=[]):
        self.actions[command_text] = (function, arguments, preconditions)

    # Perform a special action associated with this item
    def do_action(self, command_text, game_state):
        if command_text in self.actions:
            function, arguments, preconditions = self.actions[command_text]
            all_conditions_met = True
            for condition in preconditions:
                status = game_state.is_condition_satisfied(condition)
                if not status[0]:
                    all_conditions_met = False
                    print(status[1])
                    break
            if all_conditions_met:
                result = function(arguments)
                return result
        else:
            print('Cannot do the action. Try again.')
            return False

    

        