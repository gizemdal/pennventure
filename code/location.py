# Location
import string
from gameState import GameState

class Location(object):

    def __init__(self, name, description, isDiscovered=False):
        # A short name for the location
        self.name = name
        # A description of the location
        self.description = description
        # Dictionary mapping from item name to Item objects present in this location
        self.items = {}
        # List of characters who are present in this location
        self.characters = {}
        # Flag that gets set to True once this location has been visited by player
        self.isDiscovered = isDiscovered
        # Dictionary mapping from directions to other Location objects
        self.connections = {}
        # Dictionary mapping from direction to condition object in that direction
        self.blocks = {}
    
    def __eq__(self, other):
        return self.name == other.name

    # Mark the location as discovered
    def mark_discovered(self):
        self.isDiscovered = True

    # Connect another location to this location
    def add_connection(self, direction, other_location):
        # Make sure the given direction makes sense
        is_valid_direction = False
        # Compare direction
        if direction.lower() == 'north':
            other_location.connections['south'] = self
            is_valid_direction = True
        elif direction.lower() == 'south':
            other_location.connections['north'] = self
            is_valid_direction = True
        elif direction.lower() == 'east':
            other_location.connections['west'] = self
            is_valid_direction = True
        elif direction.lower() == 'west':
            other_location.connections['east'] = self
            is_valid_direction = True
        elif direction.lower() == 'up':
            other_location.connections['down'] = self
            is_valid_direction = True
        elif direction.lower() == 'down':
            other_location.connections['up'] = self
            is_valid_direction = True
        elif direction.lower() == 'in':
            other_location.connections['out'] = self
            is_valid_direction = True
        elif direction.lower() == 'out':
            other_location.connections['in'] = self
            is_valid_direction = True

        if is_valid_direction:
            self.connections[direction.lower()] = other_location
        else:
            print('Whoops.. There is no such direction! Try again.')

    # Add an item to location if player/NPC drops an item or item is located here
    def add_item(self, name, item):
        self.items[name.lower()] = item

    def check_item(self, item):
        # Check if given item is in the location
        return item.name.lower() in self.items
        
    # Remove the item from location if player/NPC uses the item or takes it
    def remove_item(self, item):
        self.items.pop(item.name)
    
    # Check if given direction is blocked at this location
    def check_block(self, direction, game_state):
        if direction not in self.blocks:
            return False
        # Condition = (condition text, condition element) tuple
        conditions = self.blocks[direction]
        for condition in conditions:
            if not game_state.is_condition_satisfied(condition):
                return True
        return False
    
    # Add a block at this location for given direction
    def add_block(self, direction, description, condition):
        if direction not in self.blocks:
            self.blocks[direction] = [condition]
        else:
            self.blocks[direction] = self.blocks[direction].append(condition)
        

        