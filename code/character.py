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
            self.curr_location.characters[self.name] = self
        self.inventory = {}
        # People that this character has met. This is a person -> relationship mapping where relationship
        # is a tuple of (short-term, long-term) relationship score.
        self.acquaintances = {}
    
    def __eq__(self, other):
        return self.id == other.id

    def met_someone(self, person_id, impression_score=0):
        self.acquaintances[person_id] = (impression_score, 0)
    
    def update_relationship(self, person_id, score):
        if person_id not in self.acquaintances:
            self.met_someone(person_id, score)
        else:
            self.acquaintances[person_id] = (self.acquaintances[person_id][0] + score, 0)
    
    def get_item(self, item):
        self.inventory[item.name.lower()] = item

    def check_item(self, item):
        # Check if item is in inventory
        return item.name.lower() in self.inventory
    
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
        self.curr_location.pop(self.name)
        self.curr_location = location
        self.curr_location.characters[self.name] = self
    
    def relationship_status(self, other):
        # MUST IMPROVE RELATIONSHIPS TO BE MULTIDIMENTIONAL
        if self.acquaintances[other.id][0] < 0:
            return 'dislike'
        elif self.acquaintances[other.id][0] >= 0 and self.acquaintances[other.id][0] < 50:
            return 'acquaintance'
        elif self.acquaintances[other.id][0] >= 50 and self.acquaintances[other.id][0] < 85:
            return 'friend'
        elif self.acquaintances[other.id][0] >= 85 and self.acquaintances[other.id][0] < 100:
            return 'good friend'

