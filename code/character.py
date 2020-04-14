# Character

import string

char_id = 0 # unique character id

class Character(object):

    def __init__(self, name="", location=None, is_player=False):
        global char_id
        self.name = name
        self.id = char_id
        char_id += 1
        # Current location of the character
        self.curr_location = location
        self.is_player = is_player
        if self.curr_location:
            self.curr_location.characters[self.name] = self
        self.inventory = {}
        # People that this character has met. This is a person -> relationship mapping where relationship
        # is a tuple of (short-term, long-term) relationship score.
        self.acquaintances = {}
    
    def __eq__(self, other):
        return self.id == other.id

    def met_someone(self, person, impression_score=0):
        self.acquaintances[person.id] = (impression_score, 0)
        person.acquaintances[self.id] = (impression_score, 0)
    
    def update_relationship(self, person, score):
        if person.id not in self.acquaintances:
            self.met_someone(person, score)
        else:
            self.acquaintances[person.id] = (self.acquaintances[person.id][0] + score, 0)
            person.acquaintances[self.id] = (person.acquaintances[self.id][0] + score, 0)
    
    def get_item(self, item):
        if item.name.lower() not in self.inventory:
            self.inventory[item.name.lower()] = item
            # Remove the item from current location
            item.location = None
            if self.curr_location:
                self.curr_location.remove_item(item)
        else:
            print('You already put this item in your inventory.')

    def check_item(self, item):
        # Check if item is in inventory
        return item.name.lower() in self.inventory
    
    def leave_item(self, item_name):
        if item_name in self.inventory:
            # First add this item to the location the character is at
            self.curr_location.add_item(item_name, self.inventory[item_name.lower()])
            # Then remove the item from character's inventory
            self.inventory.pop(item_name.lower())
        else:
            print('You do not have this item in your inventory.')

    def use_item(self, item_name):
        if item_name in self.inventory:
            # Remove the item from character's inventory
            self.inventory.pop(item_name.lower())
        else:
            print('You already used this item.')

    def set_location(self, location):
        # Set current location of the character
        if self.curr_location:
            del self.curr_location.characters[self.name]
        self.curr_location = location
        if self.curr_location:
            self.curr_location.characters[self.name] = self
        if self.is_player:
            if not self.curr_location.isDiscovered:
                self.curr_location.isDiscovered = True
    
    def relationship_status(self, other):
        if self.acquaintances[other.id][0] < 0:
            return 'dislike'
        elif self.acquaintances[other.id][0] >= 0 and self.acquaintances[other.id][0] < 50:
            return 'acquaintance'
        elif self.acquaintances[other.id][0] >= 50 and self.acquaintances[other.id][0] < 85:
            return 'friend'
        elif self.acquaintances[other.id][0] >= 85:
            return 'good friend'

    def get_items_in_scope(self):
        # Returns a list of items in the current location and in the inventory
        items_in_scope = []
        for item_name in self.curr_location.items:
            items_in_scope.append(self.curr_location.items[item_name])
        for item_name in self.inventory:
            items_in_scope.append(self.inventory[item_name])
        return items_in_scope

