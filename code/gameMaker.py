# Game Maker
# This code is responsible for providing a terminal interface for users to create their game files

# import all the classes
from gameState import GameState, PlotPoint, Plot
from dramaManager import DramaManager
from parser import Parser
from character import Character
from player import Player
from npc import NPC
from item import Item
from location import Location
from precondition import Precondition

# Import functions
from functions import *
import string

def menu_options():
    print('Options:')
    print('\ta) Add Location')
    print('\tb) Add NPC')
    print('\tc) Connect Locations')
    print('\td) Add Relationship (between characters)')
    print('\te) Add Item')
    print('\tf) Put Item to Inventory')
    print('\tg) Add Precondition')
    print('\th) Add Plot Point')
    print('\ti) Add Plot Point Adjacency')
    print('\tj) Add Block (between locations)')
    print('\tk) Add Action')
    print('\tl) Submit Game')
    print('\tm) Check Added Components')
    print('\tn) Delete Component')

def valid_location(maker):
    # First get a valid location name
    print('Please enter the name of your location:')
    loc_name = ''
    is_loc_name_valid = False
    while not is_loc_name_valid:
        try:
            loc_name = raw_input('>')
        except:
            loc_name = input('>')
        if len(loc_name) == 0:
            print('You cannot set an empty name. Please try again.')
            continue
        elif loc_name == 'ret':
            return (False, 0)
        elif loc_name == 'q':
            return (False, 1)
        elif len(loc_name) < 2:
            print('Your location name cannot be less than 2 characters. Please try again.')
            continue
        else:
            same_name_found = False
            for (loc_id, loc) in maker.locations.items():
                if loc.name.lower() == loc_name.lower():
                    same_name_found = True
                    print('You already added a location with the same name.')
                    break
            if not same_name_found:
                is_loc_name_valid = True
    # Now get a location description
    print('Please enter your location description:')
    loc_desc = ''
    try:
        loc_desc = raw_input('>')
    except:
        loc_desc = input('>')
    if loc_desc == 'ret':
        return (False, 0)
    elif loc_desc == 'q':
        return (False, 1)
    # Now determine if your location should be marked as discovered
    print("Is your location discovered by default? Enter 'yes' or 'no':")
    loc_discovered = ''
    is_loc_discovered_valid = False
    while not is_loc_discovered_valid:
        try:
            loc_discovered = raw_input('>')
        except:
            loc_discovered = input('>')
        if loc_discovered == 'ret':
            return (False, 0)
        elif loc_discovered == 'q':
            return (False, 1)
        elif loc_discovered.lower() != 'yes' and loc_discovered.lower() != 'no':
            print('Please type either yes or no.')
            continue
        else:
            is_loc_discovered_valid = True
    print('Awesome. Keep in mind that the start location of the game will be marked as discovered by default.')
    return (True, loc_name, loc_desc, loc_discovered)

def valid_character(maker):
    # First get a valid npc name
    print('Please enter the name of your NPC character:')
    npc_name = ''
    is_npc_name_valid = False
    while not is_npc_name_valid:
        try:
            npc_name = raw_input('>')
        except:
            npc_name = input('>')
        if npc_name == 'ret':
            return (False, 0)
        elif npc_name == 'q':
            return (False, 1)
        else:
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in npc_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The character name must contain at least 1 ASCII character. Please try again.')
                continue
            else:
                # Check if a character with given name already exists
                same_name_found = False
                for (npc_id, npc) in maker.characters.items():
                    if npc.name.lower() == npc_name.lower():
                        same_name_found = True
                        print('You already added a character with this name.')
                        break
                if not same_name_found:
                    is_npc_name_valid = True
    # Now set their start location
    print('Please enter the name of the (previously added) location your character should be at in the beginning of the game:')
    print('(If you want the location to be None, just hit enter without typing anything.)')
    npc_loc = ''
    loc_id = -1
    is_valid_npc_location = False
    while not is_valid_npc_location:
        try:
            npc_loc = raw_input('>')
        except:
            npc_loc = input('>')
        if npc_loc == 'ret':
            return (False, 0)
        elif npc_loc == 'q':
            return (False, 1)
        else:
            if len(npc_loc) == 0:
                # Set location to None
                loc_id = -1
                is_valid_npc_location = True
            else:
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == npc_loc.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_npc_location = True
    return (True, npc_name, loc_id)

def valid_connection(maker):
    # First get the from location
    print('Please enter the name of the location you want the direction of connection to go FROM:')
    from_loc = ''
    from_loc_id = -1
    is_from_loc_valid = False
    while not is_from_loc_valid:
        try:
            from_loc = raw_input('>')
        except:
            from_loc = input('>')
        if from_loc == 'ret':
            return (False, 0)
        elif from_loc == 'q':
            return (False, 1)
        else:
            # Check if location exists
            loc_found = False
            for loc in maker.locations.values():
                if loc.name.lower() == from_loc.lower():
                    from_loc_id = loc.id
                    loc_found = True
                    break
            if not loc_found:
                print('No such location exists. Please try again.')
                continue
            else:
                is_from_loc_valid = True
    # Now get the to location
    print('Please enter the name of the location you want the direction of connection to go TO:')
    to_loc = ''
    to_loc_id = -1
    is_to_loc_valid = False
    while not is_to_loc_valid:
        try:
            to_loc = raw_input('>')
        except:
            to_loc = input('>')
        if to_loc == 'ret':
            return (False, 0)
        elif to_loc == 'q':
            return (False, 1)
        else:
            # Check if entered location is not the same as from location
            if to_loc.lower() == from_loc.lower():
                print('Your FROM and TO location cannot be the same. Please enter a different location.')
                continue
            else:
                # Check if such location exists
                # Check if location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == to_loc.lower():
                        to_loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_to_loc_valid = True
    # Now get the direction
    print('Please enter the name of the direction. Valid directions are: north, south, east, west, in, out:')
    direc = ''
    is_valid_direc = False
    while not is_valid_direc:
        try:
            direc = raw_input('>')
        except:
            direc = input('>')
        if direc == 'ret':
            return (False, 0)
        elif direc == 'q':
            return (False, 1)
        elif direc.lower() not in ['north', 'south', 'west', 'east', 'out', 'in']:
            print('This is not a valid direction. Please try again.')
            continue
        else:
            is_valid_direc = False
    # Return the direction
    print('Awesome. Keep in mind that once a connection is added, its opposite direction will be added as well.')
    return (True, from_loc_id, to_loc_id, direc)

def valid_relationship(maker):
    print('Please enter the name of your character.') 
    print('If your character is the player, just hit enter.')
    char_name_1 = ''
    char_id_1 = 0
    is_char_1_valid = False
    while not is_char_1_valid:
        try:
            char_name_1 = raw_input('>')
        except:
            char_name_1 = input('>')
        if char_name_1 == 'ret':
            return (False, 0)
        elif char_name_1 == 'q':
            return (False, 1)
        else:
            if len(char_name_1) == 0:
                # Player
                char_id_1 = 0
                is_char_1_valid = True
            else:
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == char_name_1:
                        char_id_1 = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_char_1_valid = True
    # Now get the second character
    print('Please enter the name of the other character you want to set a relationship score with.') 
    print('If your character is the player, just hit enter.')
    char_name_2 = ''
    char_id_2 = 0
    is_char_2_valid = False
    while not is_char_2_valid:
        try:
            char_name_2 = raw_input('>')
        except:
            char_name_2 = input('>')
        if char_name_2 == 'ret':
            return (False, 0)
        elif char_name_2 == 'q':
            return (False, 1)
        else:
            # Check if second character is the same as first character
            if char_name_2.lower() == char_name_1.lower():
                print('Your other character cannot be the first character. Please try again.')
                continue
            if len(char_name_2) == 0:
                # Player
                char_id_2 = 0
                is_char_2_valid = True
            else:
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == char_name_2:
                        char_id_2 = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_char_2_valid = True
    # Now get the scores
    print('Please enter the short term relationship score (must be an integer):')
    short_term = ''
    is_short_term_valid = False
    while not is_short_term_valid:
        try:
            short_term = raw_input('>')
        except:
            short_term = input('>')
        if short_term == 'ret':
            return (False, 0)
        elif short_term == 'q':
            return (False, 1)
        else:
            # Check if something is entered
            if len(short_term) == 0:
                print('The number you entered is invalid. Please try again.')
                continue
            # Check if negative number
            is_negative = False
            if short_term[0] == '-':
                is_negative = True
            # Check if something negative is entered
            if is_negative:
                if len(short_term) == 1:
                    print('The number you entered is invalid. Please try again.')
                    continue
            # Check if entry is a number
            if is_negative:
                short_term = short_term[1:]
            valid_number = True
            for digit in short_term:
                if digit not in string.digits:
                    valid_number = False
                    break
            if not valid_number:
                print('The number you entered is invalid. Please try again.')
                continue
            short_term = int(short_term)
            is_short_term_valid = True
    print('Please enter the long term relationship score (must be an integer):')
    long_term = ''
    is_long_term_valid = False
    while not is_long_term_valid:
        try:
            long_term = raw_input('>')
        except:
            long_term = input('>')
        if long_term == 'ret':
            return (False, 0)
        elif long_term == 'q':
            return (False, 1)
        else:
            # Check if something is entered
            if len(long_term) == 0:
                print('The number you entered is invalid. Please try again.')
                continue
            # Check if negative number
            is_negative = False
            if long_term[0] == '-':
                is_negative = True
            # Check if something negative is entered
            if is_negative:
                if len(long_term) == 1:
                    print('The number you entered is invalid. Please try again.')
                    continue
            # Check if entry is a number
            if is_negative:
                long_term = long_term[1:]
            valid_number = True
            for digit in long_term:
                if digit not in string.digits:
                    valid_number = False
                    break
            if not valid_number:
                print('The number you entered is invalid. Please try again.')
                continue
            long_term = int(long_term)
            is_long_term_valid = True
    print('Perfect. Keep in mind that relationships are not symmetric.\n(e.g. if person A has short term score of 40 for person B, person B will not automatically have the same score for person A.')
    return (True, char_id_1, char_id_2, short_term, long_term)

def valid_item(maker):
    # First get the name
    print('Please enter the name of the new item:')
    item_name = ''
    is_item_name_valid = False
    while not is_item_name_valid:
        try:
            item_name = raw_input('>')
        except:
            item_name = input('>')
        if item_name == 'ret':
            return (False, 0)
        elif item_name == 'q':
            return (False, 1)
        else:
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in item_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The item name must contain at least 1 ASCII character. Please try again.')
                continue
            else:
                # Check if item name already exists
                same_name_found = False
                for (item_id, item) in maker.items.items():
                    if item.name.lower() == item_name.lower():
                        same_name_found = True
                        print('You already added an item with this name.')
                        break
                if not same_name_found:
                    is_item_name_valid = True
    # Now get the description
    print('Please enter a description for your item:')
    item_desc = ''
    try:
        item_desc = raw_input('>')
    except:
        item_desc = input('>')
    if item_desc == 'ret':
        return (False, 0)
    elif item_desc == 'q':
        return (False, 1)
    # Now get the getable status
    print("Is your item collectable? Enter 'yes' or 'no':")
    item_gettable = ''
    is_item_gettable_valid = False
    while not is_item_gettable_valid:
        try:
            item_gettable = raw_input('>')
        except:
            item_gettable = input('>')
        if item_gettable == 'ret':
            return (False, 0)
        elif item_gettable == 'q':
            return (False, 1)
        elif item_gettable.lower() != 'yes' and item_gettable.lower() != 'no':
            print('Please type either yes or no.')
            continue
        else:
            is_item_gettable_valid = True
    # Now get the examine text
    print('Please enter an examination text for your item:')
    item_ex = ''
    try:
        item_ex = raw_input('>')
    except:
        item_ex = input('>')
    if item_ex == 'ret':
        return (False, 0)
    elif item_ex == 'q':
        return (False, 1)
    # Now get the start location
    print('Please enter the name of the (previously added) location your item should be at in the beginning of the game:')
    print('(If you want the location to be None, just hit enter without typing anything.)')
    item_loc = ''
    loc_id = -1
    is_valid_item_location = False
    while not is_valid_item_location:
        try:
            item_loc = raw_input('>')
        except:
            item_loc = input('>')
        if item_loc == 'ret':
            return (False, 0)
        elif item_loc == 'q':
            return (False, 1)
        else:
            if len(item_loc) == 0:
                # Set location to None
                loc_id = -1
                is_valid_item_location = True
            else:
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == item_loc.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_item_location = True
    return (True, item_name, item_desc, item_gettable, item_ex, loc_id)

def valid_inventory(maker):
    # Get the item
    print('Please enter the name of the item you want to put in an inventory:')
    item_name = ''
    item_id = 0
    is_item_name_valid = False
    while not is_item_name_valid:
        try:
            item_name = raw_input('>')
        except:
            item_name = input('>')
        if item_name == 'ret':
            return (False, 0)
        elif item_name == 'q':
            return (False, 1)
        else:
            # Check if the item exists
            item_exists = False
            for (item_id, item) in maker.items.items():
                if item.name.lower() == item_name.lower():
                    item_exists = True
                    item_id = item.id
                    break
            if not item_exists:
                print('No such item exists. Please try again.')
                continue
            else:
                is_item_name_valid = True
    # Get the character
    print('Please enter the name of the character whose inventory you want to put this item to.')
    print('If your character is the player, just hit enter.')
    npc_name = ''
    npc_id = 0
    is_npc_name_valid = False
    while not is_npc_name_valid:
        try:
            npc_name = raw_input('>')
        except:
            npc_name = input('>')
        if npc_name == 'ret':
            return (False, 0)
        elif npc_name == 'q':
            return (False, 1)
        else:
            if len(npc_name) == 0:
                # Player
                npc_id = 0
                is_npc_name_valid = True
            else:
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == npc_name:
                        npc_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_npc_name_valid = True
    return (True, npc_id, item_id)

def valid_precondition(maker):
    print('Please enter the letter corresponding to the precondition category you would like:')
    print('Supported Preconditions:')
    print('\ta) Player in location')
    print('\tb) NPC in location')
    print('\tc) Item in player inventory')
    print('\td) Item in NPC inventory')
    print('\te) Item NOT in player inventory')
    print('\tf) Item in location')
    print('\tg) Player is friends with')
    print('\th) Player is acquaintances with')
    print('\ti) Player dislikes')
    print('\tj) Player does not dislike')
    category = ''
    is_valid_precondition = False
    while not is_valid_precondition:
        try:
            category = raw_input('>')
        except:
            category = input('>')
        if category == 'ret':
            return (False, 0)
        elif category == 'q':
            return (False, 1)
        else:
            if len(category) == 1 and category in 'abcdefghij':
                is_valid_precondition = True
            else:
                print('Invalid category. Please try again.')
    # Now determine what is needed for the precondition category
    if category == 'a':
        # Need location
        pass
    elif category == 'b':
        pass
    elif category == 'c':
        pass
    elif category == 'd':
        pass
    elif category == 'e':
        pass
    elif category == 'f':
        pass
    elif category == 'g':
        pass
    elif category == 'h':
        pass
    elif category == 'i':
        pass
    elif category == 'j':
        pass
    return (False, 1)

class GameMaker(object):

    def __init__(self):
        # object types
        self.locations = {}
        self.characters = {}
        self.player = Player('Player') # initialize player
        self.characters[self.player.id] = self.player
        self.items = {}
        self.plot_points = {}
        self.preconditions = {}
        self.plot = None
        # fields for objects
        self.blocks = []
        self.connections = []
        self.relationships = []
        self.inventory = []

    def create_game(self):
        pass
    

# Start maker here
game_maker = GameMaker()
entered = ''
print('Welcome to Game Maker. You can create game components and make your own game file to play.')
print('Enter the required information to create your components. For multiple choice options, please enter the choice letter.')
print("Once you are done adding game components, enter 'l' to create your game file.")
print("If you would like to go back to main menu while creating a component, please enter 'ret'")
print('Press q anytime to quit the game maker.')
while True:
    menu_options()
    try:
        entered = raw_input('>')
    except:
        entered = input('>')
    if entered.lower() == 'q':
        print('Goodbye')
        break
    elif entered.lower() == 'a':
        result = valid_location(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # extract the discoverablity
            is_discovered = None
            if result[3] == 'yes':
                is_discovered = True
            else:
                is_discovered = False
            # Create and add the location
            new_loc = Location(result[1], result[2], is_discovered)
            game_maker.locations[new_loc.id] = new_loc
            print(str(result[1]) + ' is added to locations!')
    elif entered.lower() == 'b':
        result = valid_character(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # extract the location
            npc_location = None
            if result[2] > -1:
                npc_location = game_maker.locations[result[2]]
            new_npc = NPC(result[1], npc_location)
            game_maker.characters[new_npc.id] = new_npc
            print(str(result[1]) + ' is added to characters!')
    elif entered.lower() == 'c':
        result = valid_connection(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # Add connection
            game_maker.connections.append((result[1], result[2], result[3]))
            print('Connection added succesfully!')
    elif entered.lower() == 'd':
        result = valid_relationship(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # Add relationship
            game_maker.relationships.append((result[1], result[2], result[3], result[4]))
            print('Relationship added succesfully!')
    elif entered.lower() == 'e':
        result = valid_item(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # extract gettable
            is_gettable = None
            if result[3] == 'yes':
                is_gettable  = True
            else:
                is_gettable  = False
             # extract the location
            item_location = None
            if result[5] > -1:
                item_location = game_maker.locations[result[5]]
            # Create item
            new_item = Item(result[1], result[2], is_gettable, result[4], item_location)
            print(str(result[1]) + ' is added to items!')
    elif entered.lower() == 'f':
        result = valid_inventory(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # Add inventory change
            game_maker.inventory.append((result[1], result[2]))
            print('Inventory change added succesfully!')
    elif entered.lower() == 'g':
        result = valid_precondition(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            pass
    elif entered.lower() == 'h':
        print('This option is not implemented yet.')
    elif entered.lower() == 'i':
        print('This option is not implemented yet.')
    elif entered.lower() == 'j':
        print('This option is not implemented yet.')
    elif entered.lower() == 'k':
        print('This option is not implemented yet.')
    elif entered.lower() == 'l':
        print('This option is not implemented yet.')
    elif entered.lower() == 'm':
        # Check added components
        # PUT THIS ALL IN ANOTHER FUNCTION
        print('Locations: ' + str([loc.name for loc in game_maker.locations.values()]))
        print('Connections: ')
        print('NPCs: ' + str([n.name for n in game_maker.characters.values()]))
        print('Items: ' + str([item.name for item in game_maker.items.values()]))
        print('Plot:')
    elif entered.lower() == 'n':
        print('This option is not implemented yet.')
    else:
        print('Cannot process your request. Please pick an option from the menu.')