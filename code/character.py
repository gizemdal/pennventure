# Character

import string

char_id = 0 # unique character id

class Character(object):

    def __init__(self, name="", location=None):
        global char_id
        self.name = name
        self.id = char_id
        char_id += 1
        # Current location of the character
        self.curr_location = location
        if self.curr_location:
            self.curr_location.characters.append(self)
        self.inventory = {}
        # People that this character has met. This is a person -> relationship mapping where relationship
        # is a tuple of (short-term, long-term) relationship score.
        self.acquaintances = {}
    
    def __eq__(self, other):
        return self.id == other.id

    def met_someone(self, person_id, impression_score=0):
        self.acquaintances[person_id] = (impression_score, 0)
    
    def get_item(self, item):
        self.inventory[item.name.lower()] = item
    
    def leave_item(self, item_name):
        # First add this item to the location the character is at
        self.curr_location.add_item(item_name, self.inventory[item_name.lower()])
        # Then remove the item from character's inventory
        self.inventory.pop(item_name.lower())

    def use_item(self, item_name):
        # Remove the item from character's inventory
        self.inventory.pop(item_name.lower())

    def set_location(self, location):
        # Set current location of the character
        self.curr_location.remove(self)
        self.curr_location = location
        self.curr_location.characters.append(self)
