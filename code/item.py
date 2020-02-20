# Item
from location import Location
import string

class Item(object):

    def __init__(self, 
                 name, 
                 description, 
                 collectable=True, 
                 examine_text="", 
                 location=None):

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
    
    # Change the location of the item
    def change_location(self, new_location):
        if self in self.location.items[self.name]:
            self.location.remove_item(self)
        self.location = new_location
        new_location.add_item(self.name, self)

    # Returns a list of special commands associated with this object
    def get_commands(self):
        return self.actions.keys()
    
    # Add a special action associated with this item
    def add_action(self, command_text, function, arguments, preconditions={}):
        self.actions[command_text] = (function, arguments, preconditions)

    # Perform a special action associated with this item
    def do_action(self, command_text, game):
        if command_text in self.actions:
            function, arguments, preconditions = self.actions[command_text]
            function(arguments, preconditions)
        else:
            print('Cannot do the action. Try again.')

    

        