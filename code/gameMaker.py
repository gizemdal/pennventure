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
from location import direction_opp

def trim_space_punc(n):
    # get rid of the white space and punctuation from given string
    new_n = ''
    for c in n:
        if c in string.whitespace or c in string.punctuation:
            continue
        new_n += c
    return new_n

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

def print_preconditions(maker, preconditions):
    print('Available preconditions: ')
    list_of_conditions = [(pre.context, pre.name) for pre in maker.preconditions.values() if pre.id not in preconditions]
    for condition in list_of_conditions:
        print('\tName: ' + str(condition[1]) + ' , Context: ' + str(condition[0]))

def print_relationships(maker):
    if len(maker.relationships) == 0:
        print('No relationship is created yet.')
    else:
        print('\nRelationships: ')
        for rel in maker.relationships:
            print(str(maker.characters[rel[0]].name) + ' -> ' + str(maker.characters[rel[1]].name) + ', Short term: ' + str(rel[2]) + ', Long term: ' + str(rel[3]))

def print_connections(maker):
    if len(maker.connections) == 0:
        print('No connection is created yet.')
    else:
        print('\nConnections: ')
        for con in maker.connections:
            print('Locations: ' + str(maker.locations[con[0]].name) + ' <-> ' + str(maker.locations[con[1]].name) + ', Direction: ' + str(con[2]) + '/' + str(direction_opp(con[2])))

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
        else:
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in loc_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The location name must contain at least 1 ASCII character. Please try again.')
                continue
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
        elif trim_space_punc(npc_name).lower() == 'player':
            print("You cannot name a NPC character 'player', please pick another name.")
            continue
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
    print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
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
    print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
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
    print('Available locations: ' + str([loc.name for loc in maker.locations.values() if loc.name.lower() != from_loc.lower()]))
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
            is_valid_direc = True
    # Return the direction
    print('Awesome. Keep in mind that once a connection is added, its opposite direction will be added as well.')
    return (True, from_loc_id, to_loc_id, direc)

def valid_relationship(maker):
    print('Please enter the name of your character.') 
    print('If your character is the player, just hit enter.')
    print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                char_name_1 = 'Player'
                is_char_1_valid = True
            else:
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == char_name_1.lower():
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
    print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player' if n.name.lower() != char_name_1.lower()]))
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
                char_name_2 = 'Player'
                is_char_2_valid = True
            else:
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == char_name_2.lower():
                        char_id_2 = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_char_2_valid = True
    # Before proceeding, check if a relationship already exists
    rel_found = False
    for rel in maker.relationships:
        if rel[0] == char_id_1 and rel[1] == char_id_2:
            rel_found = True
            break
    if rel_found:
        print('You already added a relationship for ' + char_name_1.lower() + ' with ' + char_name_2.lower() + '. If you want to overwrite this relationship, you must first delete it.')
        return (False, 0)
    # Now get the scores
    print('Please enter the short term relationship score (must be an integer).')
    print('The short term relationship score represents the relationship status of two characters in a given moment.')
    print('A short term relationship score greater than or equal to 50 is considered as friendship while much lower scores may result in dislike status.')
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
            if is_negative:
                short_term = -short_term
            is_short_term_valid = True
    print('Please enter the long term relationship score (must be an integer):')
    print('The long term relationship score represents the relationship status of two characters in the long run.')
    print('A long term relationship score greater than or equal to 50 is considered as strong friendship while much lower scores may result in strong dislike status.')
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
            if is_negative:
                long_term = -long_term
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
    print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
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
    print('Available items: ' + str([item.name for item in maker.items.values()]))
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
    print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                    if char.name.lower() == npc_name.lower():
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
    # First get the name
    print('Please enter the name of the new precondition:')
    pre_name = ''
    is_pre_name_valid = False
    while not is_pre_name_valid:
        try:
            pre_name = raw_input('>')
        except:
            pre_name = input('>')
        if pre_name == 'ret':
            return (False, 0)
        elif pre_name == 'q':
            return (False, 1)
        else:
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in pre_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The item name must contain at least 1 ASCII character. Please try again.')
                continue
            else:
                # Check if item name already exists
                same_name_found = False
                for (pre_id, pre) in maker.items.items():
                    if pre.name.lower() == pre_name.lower():
                        same_name_found = True
                        print('You already added an item with this name.')
                        break
                if not same_name_found:
                    is_pre_name_valid = True
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
        print('Enter the name of the location:')
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
        # Get player location
        player_loc = ''
        loc_id = -1
        is_valid_player_location = False
        while not is_valid_player_location:
            try:
                player_loc = raw_input('>')
            except:
                player_loc = input('>')
            if player_loc == 'ret':
                return (False, 0)
            elif player_loc == 'q':
                return (False, 1)
            else:
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == player_loc.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_player_location = True
        return (True, pre_name, 'player_in_location', loc_id)
    elif category == 'b':
        print('Enter the name of the NPC:')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
        # Get npc name
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
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == npc_name.lower():
                        npc_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_npc_name_valid = True
        print('Enter the name of the location:')
        print('If the location is None, just hit enter')
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
        # Get npc location
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
                # Check if location == None
                if len(npc_loc) == 0:
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
        return (True, pre_name, 'npc_in_location', npc_id, loc_id)
    elif category == 'c':
        # Item in player inventory
        print('Enter the name of the item:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
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
        return (True, pre_name, 'item_in_player_inventory', item_id)
    elif category == 'd':
        # Item in NPC inventory
        print('Enter the name of the item:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
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
        # Get the NPC
        print('Enter the name of the NPC:')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == npc_name.lower():
                        npc_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_npc_name_valid = True
        return (True, pre_name, 'item_in_npc_inventory', npc_id, item_id)
    elif category == 'e':
        # Get item name
        print('Enter the name of the item:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
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
        return (True, pre_name, 'item_not_in_player_inventory', item_id)
    elif category == 'f':
        # Get the item
        print('Enter the name of the item:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
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
        # Get the location
        print('Please enter the location name:')
        print('(If you want the location to be None, just hit enter without typing anything.)')
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
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
        return (True, pre_name, 'item_in_location', loc_id, item_id)
    elif category in 'ghij':
        # Get the NPC
        print('Enter the name of the NPC:')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == npc_name.lower():
                        npc_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_npc_name_valid = True
        if category == 'g':
            return (True, pre_name, 'player_is_friends_with', npc_id)
        elif category == 'h':
            return (True, pre_name, 'player_is_acquaintances_with', npc_id)
        elif category == 'i':
            return (True, pre_name, 'player_dislikes', npc_id)
        elif category == 'j':
            return (True, pre_name, 'player_does_not_dislike', npc_id)
        else:
            return (False, 0)
    else:  
        return (False, 0)

def query_npc(maker):
    print('Please enter the name of the NPC:')
    print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
            # Check if character exists
            char_found = False
            for char in maker.characters.values():
                if char.id == 0:
                    continue
                if char.name.lower() == npc_name.lower():
                    npc_id = char.id
                    char_found = True
                    break
            if not char_found:
                print('You do not have a character with this name. Please try again.')
                continue
            else:
                is_npc_name_valid = True
    return (True, npc_id)

def query_location(maker):
    print('Please enter the location name:')
    print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
    loc_name = ''
    loc_id = -1
    is_valid_location_name = False
    while not is_valid_location_name:
        try:
            loc_name = raw_input('>')
        except:
            loc_name = input('>')
        if loc_name == 'ret':
            return (False, 0)
        elif loc_name == 'q':
            return (False, 1)
        else:
            if len(loc_name) == 0:
                print("Use the 'Set NPC Location to None' category for this. Please try again.")
            else:
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == loc_name.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_location_name = True
    return (True, loc_id)


def valid_plot_point(maker):
    print('Welcome to plot point maker! Here you can create plot points for your plot graph to be used by the drama manager.')
    print('Although the point adjacencies has to be defined later, the very first plot point you create will be your starting point by default.')
    print('Please enter a name for your new plot point:')
    plot_name = ''
    is_valid_plot_name = False
    while not is_valid_plot_name:
        try:
            plot_name = raw_input('>')
        except:
            plot_name = input('>')
        if plot_name == 'ret':
            return (False, 0)
        elif plot_name == 'q':
            return (False, 1)
        else:
            # Plot names must have at least one ASCII character   
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in plot_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The plot point name must contain at least 1 ASCII character. Please try again.')
                continue
            else:
                # Check if plot name already exists
                same_name_found = False
                for (plot_id, plot) in maker.plot_points.items():
                    if plot.name.lower() == plot_name.lower():
                        same_name_found = True
                        print('You already added a plot point with this name.')
                        break
                if not same_name_found:
                    is_valid_plot_name = True
    print('Write a text that should be printed once the player reaches this plot point.')
    print('If you do not want to add any text, just hit Enter.')
    message = ''
    try:
        message = raw_input('>')
    except:
        message = input('>')
    if plot_name == 'ret':
        return (False, 0)
    elif plot_name == 'q':
        return (False, 1)
    print('Do you want the game to end when player reaches this plot point?')
    print("Please enter either 'yes' or 'no':")
    is_end = ''
    is_valid_end = False
    while not is_valid_end:
        try:
            is_end = raw_input('>')
        except:
            is_end = input('>')
        if is_end == 'ret':
            return (False, 0)
        elif is_end == 'q':
            return (False, 1)
        else:
            if is_end.lower() == 'yes' or is_end.lower() == 'no':
                is_valid_end = True
            else:
                print("Please enter either 'yes' or 'no'.")
                continue
    changes = []
    category = ''
    is_changes_done = False
    print('Please pick one of the categories below. If you are done adding changes or do not want to add any at all, just hit Enter.')
    print('\ta) Set NPC location to None')
    print('\tb) Bring NPC to location')
    while not is_changes_done:
        try:
            category = raw_input('>')
        except:
            category = input('>')
        if category == 'ret':
            return (False, 0)
        elif category == 'q':
            return (False, 1)
        else:
            if len(category) == 0:
                # User pressed Enter, done adding
                is_changes_done = True
            else:
                if category == 'a':
                    # Set NPC location to None
                    info = query_npc(maker)
                    if not info[0]:
                        return info
                    else:
                        changes.append(('set_npc_location_none', info[1]))
                        print('Set NPC location to None change added!')
                        print('Please pick one of the categories below. If you are done adding changes or do not want to add any at all, just hit Enter.')
                        print('\ta) Set NPC location to None')
                        print('\tb) Bring NPC to location')
                elif category == 'b':
                    # Bring NPC to location
                    info = query_npc(maker)
                    if not info[0]:
                        return info
                    else:
                        info_2 = query_location(maker)
                        if not info_2[0]:
                            return info_2
                        else:
                            changes.append(('bring_npc_to', info[1], info_2[1]))
                            print('Bring NPC to location change added!')
                            print('Please pick one of the categories below. If you are done adding changes or do not want to add any at all, just hit Enter.')
                            print('\ta) Set NPC location to None')
                            print('\tb) Bring NPC to location')
                else:
                    print('Invalid category! Please try again.')
    # return everything
    return (True, plot_name, is_end, changes, message)

def valid_adjacency(maker):
    print('Please enter the name of the FROM plot point:')
    print('Available plot points: ' + str([plot.name for plot in maker.plot_points.values()]))
    from_plot = ''
    from_plot_id = -1
    is_from_plot_valid = False
    while not is_from_plot_valid:
        try:
            from_plot = raw_input('>')
        except:
            from_plot = input('>')
        if from_plot == 'ret':
            return (False, 0)
        elif from_plot == 'q':
            return (False, 1)
        else:
            # Check if plot name exists
            plot_found = False
            for (plot_id, plot) in maker.plot_points.items():
                if plot.name.lower() == from_plot.lower():
                    from_plot_id = plot.id
                    plot_found = True
                    break
            if not plot_found:
                print('No such plot point exists. Please try again.')
            else:
                is_from_plot_valid = True
    print('Please enter the name of the TO plot point:')
    print('Available plot points: ' + str([plot.name for plot in maker.plot_points.values() if plot.name.lower() != from_plot.lower()]))
    to_plot = ''
    to_plot_id = -1
    is_to_plot_valid = False
    while not is_to_plot_valid:
        try:
            to_plot = raw_input('>')
        except:
            to_plot = input('>')
        if to_plot == 'ret':
            return (False, 0)
        elif to_plot == 'q':
            return (False, 1)
        else:
            # from and to cannot be the same
            if to_plot.lower() == from_plot.lower():
                print('FROM and TO plot points cannot be the same. Please try again.')
                continue
            # Check if plot name exists
            plot_found = False
            for (plot_id, plot) in maker.plot_points.items():
                if plot.name.lower() == to_plot.lower():
                    to_plot_id = plot.id
                    plot_found = True
                    break
            if not plot_found:
                print('No such plot point exists. Please try again.')
            else:
                is_to_plot_valid = True
    print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
    print('If you are done adding preconditions, just hit Enter.')
    print_preconditions(maker, [])
    preconditions = []
    is_preconditions_done = False
    pre_name = ''
    pre_id = -1
    while not is_preconditions_done:
        try:
            pre_name = raw_input('>')
        except:
            pre_name = input('>')
        if pre_name == 'ret':
            return (False, 0)
        elif pre_name == 'q':
            return (False, 1)
        else:
            if len(pre_name) == 0:
                # User hit Enter
                is_preconditions_done = True
                continue
            # Check if precondition exists
            pre_found = False
            for (cond_id, pre) in maker.preconditions.items():
                if pre.name.lower() == pre_name.lower():
                    pre_id = cond_id
                    pre_found = True
                    break
            if not pre_found:
                print('No such precondition exists. Please try again.')
                print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
                print('If you are done adding preconditions, just hit Enter.')
                print_preconditions(maker, preconditions)
            else:
                # Check if this precondition was already added
                if pre_id in preconditions:
                    print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                    print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    preconditions.append(pre_id)
                    print('Precondition added successfully!')
                    print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
    return (True, from_plot_id, to_plot_id, preconditions)

def valid_block(maker):
    print('Please enter the name of the location for the block:')
    print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
    loc_name = ''
    loc_id = -1
    is_valid_location_name = False
    while not is_valid_location_name:
        try:
            loc_name = raw_input('>')
        except:
            loc_name = input('>')
        if loc_name == 'ret':
            return (False, 0)
        elif loc_name == 'q':
            return (False, 1)
        else:
            # Check if such location exists
            loc_found = False
            for loc in maker.locations.values():
                if loc.name.lower() == loc_name.lower():
                    loc_id = loc.id
                    loc_found = True
                    break
            if not loc_found:
                print('No such location exists. Please try again.')
                continue
            else:
                is_valid_location_name = True
    print('Please pick the direction of the block from your location.')
    print('(If you do not see any directions, it could be either because you have no connections from this location yet or you already added blocks to available directions.)')
    from_available = [con[2] for con in maker.connections if con[0] == loc_id]
    valid_available_from = [direc for direc in from_available if direc not in [block[1] for block in maker.blocks]]
    to_available = [con[2] for con in maker.connections if con[1] == loc_id]
    valid_available_to = [direction_opp(direc) for direc in to_available if direction_opp(direc) not in [block[1] for block in maker.blocks]]
    total_available = valid_available_from + valid_available_to
    print('Available directions: ' + str(total_available))
    direction = ''
    is_valid_direction = False
    while not is_valid_direction:
        try:
            direction = raw_input('>')
        except:
            direction = input('>')
        if direction == 'ret':
            return (False, 0)
        elif direction == 'q':
            return (False, 1)
        else:
            if direction not in total_available:
                print('Invalid direction. Please try again.')
            else:
                is_valid_direction = True
    print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
    print('If you are done adding preconditions, just hit Enter.')
    print_preconditions(maker, [])
    preconditions = []
    is_preconditions_done = False
    pre_name = ''
    pre_id = -1
    while not is_preconditions_done:
        try:
            pre_name = raw_input('>')
        except:
            pre_name = input('>')
        if pre_name == 'ret':
            return (False, 0)
        elif pre_name == 'q':
            return (False, 1)
        else:
            if len(pre_name) == 0:
                # User hit Enter
                is_preconditions_done = True
                continue
            # Check if precondition exists
            pre_found = False
            for (cond_id, pre) in maker.preconditions.items():
                if pre.name.lower() == pre_name.lower():
                    pre_id = cond_id
                    pre_found = True
                    break
            if not pre_found:
                print('No such precondition exists. Please try again.')
                print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
                print('If you are done adding preconditions, just hit Enter.')
                print_preconditions(maker, preconditions)
            else:
                # Check if this precondition was already added
                if pre_id in preconditions:
                    print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                    print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    preconditions.append(pre_id)
                    print('Precondition added successfully!')
                    print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
    return (True, loc_id, direction, preconditions)

def valid_action(maker):
    print('Would you like to add an action to an item or a NPC character?')
    print('\ta) Item')
    print('\tb) NPC')
    subject = ''
    is_valid_subject = False
    while not is_valid_subject:
        try:
            subject = raw_input('>')
        except:
            subject = input('>')
        if subject == 'ret':
            return (False, 0)
        elif subject == 'q':
            return (False, 1)
        else:
            if len(subject) == 1 and subject in 'ab':
                is_valid_subject = True
            else:
                print('Invalid option! Please try again.')
    if subject == 'a':
        print('Please enter the item name:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
        subject = 0
    elif subject == 'b':
        print('Please enter the NPC name:')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
        subject = 1
    subject_name = ''
    subject_id = -1
    is_subject_name_valid = False
    while not is_subject_name_valid:
        try:
            subject_name = raw_input('>')
        except:
            subject_name = input('>')
        if subject_name == 'ret':
            return (False, 0)
        elif subject_name == 'q':
            return (False, 1)
        else:
            if subject == 0:
                # Item: check if item exists
                item_exists = False
                for (item_id, item) in maker.items.items():
                    if item.name.lower() == subject_name.lower():
                        item_exists = True
                        subject_id = item.id
                        break
                if not item_exists:
                    print('No such item exists. Please try again.')
                    continue
                else:
                    is_subject_name_valid = True
            elif subject == 1:
                # NPC: check if NPC exists
                npc_exists = False
                for (npc_id, npc) in maker.characters.items():
                    if npc.name.lower() == subject_name.lower():
                        npc_exists = True
                        subject_id = npc.id
                        break
                if not npc_exists:
                    print('There is no NPC with this name. Please try again.')
                    continue
                else:
                    is_subject_name_valid = True
            else:
                print('Bug here')
                return (False, 0)
    print('Please enter the corresponding letter for an action from the menu below:')
    print('Actions:')
    print('\ta) Describe something')
    print('\tb) Call NPC to Location')
    print('\tc) Interact with Person')
    print('\td) Ask for Item')
    print('\te) Redeem Item')
    action = ''
    is_valid_action = False
    while not is_valid_action:
        try:
            action = raw_input('>')
        except:
            action = input('>')
        if action == 'ret':
            return (False, 0)
        elif action == 'q':
            return (False, 1)
        else:
            if len(action) == 1 and action in 'abcde':
                is_valid_action = True
            else:
                print('Invalid action! Please try again.')
    # Get command name
    print('What would you like to name this action command?')
    command_name = ''
    is_command_name_valid = False
    while not is_command_name_valid:
        try:
            command_name = raw_input('>')
        except:
            command_name = input('>')
        if command_name == 'ret':
            return (False, 0)
        elif command_name == 'q':
            return (False, 1)
        else:
            # Check if the name contains at least one ascii characher
            ascii_found = False
            for c in command_name:
                if c.lower() in string.ascii_lowercase:
                    ascii_found = True
                    break
            if not ascii_found:
                print('The command name must contain at least 1 ASCII character. Please try again.')
                continue
            else:
                is_command_name_valid = True
    # Get the arguments
    if action == 'a':
        # Describe something
        print('Please write a description to print when this command is called:')
        description = ''
        try:
            description = raw_input('>')
        except:
            description = input('>')
        if description == 'ret':
            return (False, 0)
        elif description == 'q':
            return (False, 1)
        # Get preconditions
        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
        print('If you are done adding preconditions, just hit Enter.')
        print_preconditions(maker, [])
        preconditions = []
        is_preconditions_done = False
        pre_name = ''
        pre_id = -1
        while not is_preconditions_done:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                if len(pre_name) == 0:
                    # User hit Enter
                    is_preconditions_done = True
                    continue
                # Check if precondition exists
                pre_found = False
                for (cond_id, pre) in maker.preconditions.items():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = cond_id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    # Check if this precondition was already added
                    if pre_id in preconditions:
                        print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
                    else:
                        preconditions.append(pre_id)
                        print('Precondition added successfully!')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
        return (True, subject, subject_id, command_name, 'describe something', description, preconditions)
    elif action == 'b':
        # Call NPC to Location
        # Get location
        print('Please enter the location name:')
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
        print('(If you want the location to be None just hit Enter.)')
        loc_name = ''
        loc_id = -1
        is_valid_location_name = False
        while not is_valid_location_name:
            try:
                loc_name = raw_input('>')
            except:
                loc_name = input('>')
            if loc_name == 'ret':
                return (False, 0)
            elif loc_name == 'q':
                return (False, 1)
            else:
                if len(loc_name) == 0:
                    # hit Enter
                    loc_id = -1
                    is_valid_location_name = True
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == loc_name.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_location_name = True
        # Get NPC
        print('Please enter the name of the NPC:')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == npc_name.lower():
                        npc_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_npc_name_valid = True
        # Get action description
        print('Please enter a description to be printed if the action is successful:')
        description = ''
        try:
            description = raw_input('>')
        except:
            description = input('>')
        if description == 'ret':
            return (False, 0)
        elif description == 'q':
            return (False, 1)
        # Get action repeated description
        print('Please enter a description to be printed if the action is repeated:')
        repeated = ''
        try:
            repeated = raw_input('>')
        except:
            repeated = input('>')
        if repeated == 'ret':
            return (False, 0)
        elif repeated == 'q':
            return (False, 1)
        # Get the preconditions
        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
        print('If you are done adding preconditions, just hit Enter.')
        print_preconditions(maker, [])
        preconditions = []
        is_preconditions_done = False
        pre_name = ''
        pre_id = -1
        while not is_preconditions_done:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                if len(pre_name) == 0:
                    # User hit Enter
                    is_preconditions_done = True
                    continue
                # Check if precondition exists
                pre_found = False
                for (cond_id, pre) in maker.preconditions.items():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = cond_id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    # Check if this precondition was already added
                    if pre_id in preconditions:
                        print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
                    else:
                        preconditions.append(pre_id)
                        print('Precondition added successfully!')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
        return (True, subject, subject_id, command_name, 'call to location', loc_id, npc_id, description, repeated, preconditions)
    elif action == 'c':
        print('Please enter the name of your character.') 
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                        if char.name.lower() == char_name_1.lower():
                            char_id_1 = char.id
                            char_found = True
                            break
                    if not char_found:
                        print('You do not have a character with this name. Please try again.')
                        continue
                    else:
                        is_char_1_valid = True
        # Now get the second character
        print('Please enter the name of the other character you want to set an interaction with.') 
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player' if n.name.lower() != char_name_1.lower()]))
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
                        if char.name.lower() == char_name_2.lower():
                            char_id_2 = char.id
                            char_found = True
                            break
                    if not char_found:
                        print('You do not have a character with this name. Please try again.')
                        continue
                    else:
                        is_char_2_valid = True
        # Now get the scores
        print('Please enter a relationship score for this interaction (must be an integer):')
        print('(This score will alter the short term relationship between two characters)')
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
                if is_negative:
                    short_term = -short_term
                is_short_term_valid = True
        # Get action description
        print('Please enter a description to be printed if the action is successful:')
        description = ''
        try:
            description = raw_input('>')
        except:
            description = input('>')
        if description == 'ret':
            return (False, 0)
        elif description == 'q':
            return (False, 1)
        # Get the preconditions
        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
        print('If you are done adding preconditions, just hit Enter.')
        print_preconditions(maker, [])
        preconditions = []
        is_preconditions_done = False
        pre_name = ''
        pre_id = -1
        while not is_preconditions_done:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                if len(pre_name) == 0:
                    # User hit Enter
                    is_preconditions_done = True
                    continue
                # Check if precondition exists
                pre_found = False
                for (cond_id, pre) in maker.preconditions.items():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = cond_id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    # Check if this precondition was already added
                    if pre_id in preconditions:
                        print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
                    else:
                        preconditions.append(pre_id)
                        print('Precondition added successfully!')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
        return (True, subject, subject_id, command_name, 'interaction with person', char_id_1, char_id_2, short_term, description, preconditions)
    elif action == 'd':
        # Ask for Item
        print('Please enter the name of your character.') 
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                        if char.name.lower() == char_name_1.lower():
                            char_id_1 = char.id
                            char_found = True
                            break
                    if not char_found:
                        print('You do not have a character with this name. Please try again.')
                        continue
                    else:
                        is_char_1_valid = True
        # Now get the second character
        print('Please enter the name of the other character the first character should get an item from.') 
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player' if n.name.lower() != char_name_1.lower()]))
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
                        if char.name.lower() == char_name_2.lower():
                            char_id_2 = char.id
                            char_found = True
                            break
                    if not char_found:
                        print('You do not have a character with this name. Please try again.')
                        continue
                    else:
                        is_char_2_valid = True
        print('Please enter the name of the item for the action:')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
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
        # Get action description
        print('Please enter a description to be printed if the action is successful:')
        description = ''
        try:
            description = raw_input('>')
        except:
            description = input('>')
        if description == 'ret':
            return (False, 0)
        elif description == 'q':
            return (False, 1)
        # Get action repeated description
        print('Please enter a description to be printed if the action is repeated:')
        repeated = ''
        try:
            repeated = raw_input('>')
        except:
            repeated = input('>')
        if repeated == 'ret':
            return (False, 0)
        elif repeated == 'q':
            return (False, 1)
        # Get the preconditions
        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
        print('If you are done adding preconditions, just hit Enter.')
        print_preconditions(maker, [])
        preconditions = []
        is_preconditions_done = False
        pre_name = ''
        pre_id = -1
        while not is_preconditions_done:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                if len(pre_name) == 0:
                    # User hit Enter
                    is_preconditions_done = True
                    continue
                # Check if precondition exists
                pre_found = False
                for (cond_id, pre) in maker.preconditions.items():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = cond_id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    # Check if this precondition was already added
                    if pre_id in preconditions:
                        print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
                    else:
                        preconditions.append(pre_id)
                        print('Precondition added successfully!')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
        return (True, subject, subject_id, command_name, 'ask for item', char_id_1, char_id_2, item_id, description, repeated, preconditions)
    elif action == 'e':
        # Redeem Item
        print('Please enter the name of your character.') 
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
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
                        if char.name.lower() == char_name_1.lower():
                            char_id_1 = char.id
                            char_found = True
                            break
                    if not char_found:
                        print('You do not have a character with this name. Please try again.')
                        continue
                    else:
                        is_char_1_valid = True
        print('Please enter the name of the item to buy (if the action is successful):')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
        buy_name = ''
        buy_id = 0
        is_buy_name_valid = False
        while not is_buy_name_valid:
            try:
                buy_name = raw_input('>')
            except:
                buy_name = input('>')
            if buy_name == 'ret':
                return (False, 0)
            elif buy_name == 'q':
                return (False, 1)
            else:
                # Check if the item exists
                buy_exists = False
                for (buy_id, item) in maker.items.items():
                    if item.name.lower() == buy_name.lower():
                        buy_exists = True
                        buy_id = item.id
                        break
                if not buy_exists:
                    print('No such item exists. Please try again.')
                    continue
                else:
                    is_buy_name_valid = True
        print('Please enter the name of the item to use (if the action is successful):')
        print('Available items: ' + str([item.name for item in maker.items.values() if item.id != buy_id]))
        use_name = ''
        use_id = 0
        is_use_name_valid = False
        while not is_use_name_valid:
            try:
                use_name = raw_input('>')
            except:
                use_name = input('>')
            if use_name == 'ret':
                return (False, 0)
            elif use_name == 'q':
                return (False, 1)
            else:
                # Check if the item is the same as buy item
                if use_name.lower() == buy_name.lower():
                    print('Your buy and use items cannot be the same. Please try again.')
                    continue
                # Check if the item exists
                use_exists = False
                for (use_id, item) in maker.items.items():
                    if item.name.lower() == use_name.lower():
                        use_exists = True
                        use_id = item.id
                        break
                if not use_exists:
                    print('No such item exists. Please try again.')
                    continue
                else:
                    is_use_name_valid = True
        # Get action description
        print('Please enter a description to be printed if the action is successful:')
        description = ''
        try:
            description = raw_input('>')
        except:
            description = input('>')
        if description == 'ret':
            return (False, 0)
        elif description == 'q':
            return (False, 1)
        # Get the preconditions
        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
        print('If you are done adding preconditions, just hit Enter.')
        print_preconditions(maker, [])
        preconditions = []
        is_preconditions_done = False
        pre_name = ''
        pre_id = -1
        while not is_preconditions_done:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                if len(pre_name) == 0:
                    # User hit Enter
                    is_preconditions_done = True
                    continue
                # Check if precondition exists
                pre_found = False
                for (cond_id, pre) in maker.preconditions.items():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = cond_id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print_preconditions(maker, preconditions)
                else:
                    # Check if this precondition was already added
                    if pre_id in preconditions:
                        print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
                    else:
                        preconditions.append(pre_id)
                        print('Precondition added successfully!')
                        print('Please enter the name of the preconditions you would like to attach to this action one at a time.')
                        print('If you are done adding preconditions, just hit Enter.')
                        print_preconditions(maker, preconditions)
        return (True, subject, subject_id, command_name, 'redeem item', char_id_1, buy_id, use_id, description, preconditions)
    else:
        return (False, 0)

def valid_delete(maker):
    # Not everything can be deleted, item to be deleted must not have any dependents
    to_delete = ''
    # Print all possibilities
    print('What component would you like to delete?')
    print('(Note: Keep in mind that deleting the starting plot point is not allowed once it is added)')
    print('\ta) Location')
    print('\tb) NPC')
    print('\tc) Location connection')
    print('\td) Relationship')
    print('\te) Item')
    print('\tf) Item from an inventory')
    print('\tg) Precondition')
    print('\th) Plot Point')
    print('\ti) Plot Point Adjacency')
    print('\tj) Block (between locations)')
    print('\tk) Action')
    is_context_valid = False
    while not is_context_valid:
        try:
            to_delete = raw_input('>')
        except:
            to_delete = input('>')
        if to_delete == 'ret':
            return (False, 0)
        elif to_delete == 'q':
            return (False, 1)
        else:
            if len(to_delete) == 1 and to_delete in 'abcdefghijk':
                is_context_valid = True
            else:
                print('Invalid component! Try again.')
    if to_delete == 'a':
        # Location
        # Get the location
        print('Please enter the name of the location to be deleted:')
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
        loc_name = ''
        loc_id = -1
        is_valid_location_name = False
        while not is_valid_location_name:
            try:
                loc_name = raw_input('>')
            except:
                loc_name = input('>')
            if loc_name == 'ret':
                return (False, 0)
            elif loc_name == 'q':
                return (False, 1)
            else:
                # Check if such location exists
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == loc_name.lower():
                        loc_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_location_name = True
        # Must check if this location has dependents such as item, npc, precondition, plot point, block, connection, action
        # Check if any item is dependent
        dependency_found = False
        item_found = ''
        for (item_id, item) in maker.items.items():
            if item.location:
                if item.location.id == loc_id:
                    dependency_found = True
                    item_found = item.name
                    break
        if dependency_found:
            print('You have ' + item_found +  ' in this location. You cannot delete ' + loc_name + ' until this item is removed.')
            return (False, 0)
        # Check if any npc is dependent
        npc_found = ''
        for (npc_id, npc) in maker.characters.items():
            if npc.id == 0:
                continue
            if npc.curr_location:
                if npc.curr_location.id == loc_id:
                    dependency_found = True
                    npc_found = npc.name
                    break
        if dependency_found:
            print(npc_found + ' is in this location. You cannot delete ' + loc_name + ' until this NPC is removed.')
            return (False, 0)
        # Check if any precondition is dependent
        pre_found = ''
        pre_context = ''
        for (pre_id, pre) in maker.preconditions.items():
            for e in pre.elems:
                if type(e) is Location:
                    if e.id == loc_id:
                        dependency_found = True
                        pre_found = pre.name
                        pre_context = pre.context
                        break
        if dependency_found:
            print('You have a ' + pre_context + ' precondition named ' + pre_found + ' that contains this location. You cannot delete ' + loc_name + ' until this precondition is removed.')
            return (False, 0)
        # Check if any connection is dependent
        con_loc = ''
        for con in maker.connections:
            if con[0] == loc_id:
                dependency_found = True
                con_loc = maker.locations[con[1]].name
                break
            elif con[1] == loc_id:
                dependency_found = True
                con_loc = maker.locations[con[0]].name
                break
        if dependency_found:
            print('You have a connection with ' + con_loc + ' from this location. You cannot delete ' + loc_name + ' until this connection is removed.')
            return (False, 0)
        # Check if any block is dependent
        block_dir = ''
        for block in maker.blocks:
            if block[0] == loc_id:
                dependency_found = True
                block_dir = block[1]
                break
            else:
                # Check if any connection with this location in it exists
                for con in maker.connections:
                    if con[0] == loc_id and direction_opp(block[1]) == con[2]:
                        dependency_found = True
                        block_dir = direction_opp(block[1])
                        break
                    elif con[1] == loc_id and direction_opp(block[1]) == con[2]:
                        dependency_found = True
                        block_dir = direction_opp(block[1])
                        break
                if dependency_found:
                    break
        if dependency_found:
            print('You have a block in the ' + block_dir + ' direction from this location. You cannot delete ' + loc_name + ' until this block is removed.')
            return (False, 0)
        # Check if any plot point is dependent
        plot_point = ''
        for (plot_id, plot) in maker.plot_points.items():
            for change in plot.changes:
                if change[0] == 'bring_npc_to':
                    if change[2] == loc_id:
                        dependency_found = True
                        plot_point = plot.name
                        break
            if dependency_found:
                break
        if dependency_found:
            print('You have a plot point ' + plot_point + ' with at least 1 bring_npc_to change dependent on this location. You cannot delete ' + loc_name + ' until this plot point is removed.')
            return (False, 0)
        # Check if any action is dependent
        action_name = ''
        for action in maker.actions:
            if action[3] == 'call to location':
                if action[4] == loc_id:
                    dependency_found = True
                    action_name = action[2]
                    break
        if dependency_found:
            print('You have an action ' + action_name + " of category 'call to location' dependent on this location. You cannot delete " + loc_name + ' until this plot point is removed.')
            return (False, 0)
        # At this point there are no dependents left
        print('Location ' + maker.locations[loc_id].name + ' is deleted successfully!')
        del maker.locations[loc_id]
        return (True)
    elif to_delete == 'b':
        # Get the NPC
        print('Please enter the name of your character.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
        char_name = ''
        char_id = 0
        is_char_valid = False
        while not is_char_valid:
            try:
                char_name = raw_input('>')
            except:
                char_name = input('>')
            if char_name == 'ret':
                return (False, 0)
            elif char_name == 'q':
                return (False, 1)
            else:
                if len(char_name) == 0 or char_name.lower() == 'player':
                    print('You cannot delete the player.')
                    continue
                # Check if character exists
                char_found = False
                for char in maker.characters.values():
                    if char.id == 0:
                        continue
                    if char.name.lower() == char_name.lower():
                        char_id = char.id
                        char_found = True
                        break
                if not char_found:
                    print('You do not have a character with this name. Please try again.')
                    continue
                else:
                    is_char_valid = True
        # Possible dependencies: relationship, inventory, precondition, plot point, action
        dependency_found = False
        rel_char = ''
        dependency_text = ''
        # Check if a relationship is dependent
        for relationship in maker.relationships:
            if relationship[0] == char_id:
                rel_char = maker.characters[relationship[1]].name
                dependency_found = True
                dependency_text = char_name + ' has a relationship with ' + rel_char + '. You cannot delete ' + char_name + ' until this relationship is removed.'
                break
            elif relationship[1] == char_id:
                dependency_found = True
                dependency_text = maker.characters[relationship[0]].name + ' has a relationship with ' + char_name + '. You cannot delete ' + char_name + ' until this relationship is removed.'
                break
        if dependency_found:
            print(dependency_text)
            return (False, 0)
        # Check if an inventory is dependent
        item_name = ''
        for i in maker.inventory:
            if i[0] == char_id:
                item_name = maker.items[i[1]]
                dependency_found = True
                break
        if dependency_found:
            print('The item ' + item_name + ' is in this character\'s inventory. You cannot delete ' + char_name + ' until this inventory change is removed.')
            return (False, 0)
        # Check if a precondition is dependent
        pre_found = ''
        pre_context = ''
        for (pre_id, pre) in maker.preconditions.items():
            for e in pre.elems:
                if type(e) is NPC:
                    if e.id == char_id:
                        dependency_found = True
                        pre_found = pre.name
                        pre_context = pre.context
                        break
        if dependency_found:
            print('You have a ' + pre_context + ' precondition named ' + pre_found + ' that contains this character. You cannot delete ' + char_name + ' until this precondition is removed.')
            return (False, 0)
        # Check if a plot point is dependent
        plot_point = ''
        for (plot_id, plot) in maker.plot_points.items():
            for change in plot.changes:
                if change[1] == char_id:
                    dependency_found = True
                    plot_point = plot.name
                    break
            if dependency_found:
                break
        if dependency_found:
            print('You have a plot point ' + plot_point + ' with at least 1 change dependent on this character. You cannot delete ' + char_name + ' until this plot point is removed.')
            return (False, 0)
        # Check if an action is dependent
        action_name = ''
        for action in maker.actions:
            if action[0] == 1:
                if action[1] == char_id:
                    dependency_found = True
                    action_name = action[2]
                    break
            if action[3] == 'call to location':
                if action[5] == char_id:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'interaction with person':
                if action[4] == char_id or action[5] == char_id:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'ask for item':
                if action[4] == char_id or action[5] == char_id:
                    dependency_found = True
                    action_name = action[2]
                    break
        if dependency_found:
            print('You have the action ' + action_name + " dependent on this NPC. You cannot delete " + char_name + ' until this action is removed.')
            return (False, 0)
        # At the point there are no dependents left
        print('NPC ' + maker.characters[char_id].name + ' is deleted successfully!')
        del maker.characters[char_id]
        return (True)
    elif to_delete == 'c':
        # Delete connection
        print("Enter the names of the two locations between which the connection to delete exists. Separate the names by ','")
        print('Available locations: ' + str([loc.name for loc in maker.locations.values()]))
        loc_1_id = -1
        loc_2_id = -1
        entered_locs = ''
        is_valid_locs = False
        while not is_valid_locs:
            try:
                entered_locs = raw_input('>')
            except:
                entered_locs = input('>')
            if entered_locs == 'ret':
                return (False, 0)
            elif entered_locs == 'q':
                return (False, 1)
            else:
                splitted = entered_locs.split(',')
                if len(splitted) != 2:
                    print('Invalid format. Please re-enter the 2 location names by comma separation.')
                    continue
                # Check if locations exist
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == splitted[0].lower():
                        loc_1_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print(splitted[0] + ' does not exist. Please try again.')
                    continue
                loc_found = False
                for loc in maker.locations.values():
                    if loc.name.lower() == splitted[1].lower():
                        loc_2_id = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print(splitted[1] + ' does not exist. Please try again.')
                    continue
                is_valid_locs = True
        # Check if a connection exists between these locations
        connect_found = False
        direction = ''
        idx = 0
        for con in maker.connections:
            if con[0] == loc_1_id and con[1] == loc_2_id:
                connect_found = True
                direction = con[2]
                break
            idx += 1
        if not connect_found:
            print('There is no connection between given locations. Please try again with a different entry.')
            return (False, 0)
        print('Connections along directions ' + direction + ' and ' + direction_opp(direction) + ' between ' + maker.locations[loc_1_id].name + ' and ' + maker.locations[loc_2_id].name + ' are removed successfully!')
        maker.connections.pop(idx)
        return (True)
    elif to_delete == 'd':
        # Delete relationship
        print('Please enter the name of the character you would like to delete the relationship from.')
        print('If your character is the player, just hit enter.')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
        first_name = ''
        is_first_valid = False
        first_id = 0
        while not is_first_valid:
            try:
                first_name = raw_input('>')
            except:
                first_name = input('>')
            if first_name == 'ret':
                return (False, 0)
            elif first_name == 'q':
                return (False, 1)
            if len(first_name) == 0:
                # Player
                first_id = 0
                first_name = 'Player'
                is_first_valid = True
            else:
                # Check if a npc with given name exists
                npc_exists = False
                for char in maker.characters.values():
                    if char.name.lower() == first_name.lower():
                        npc_exists = True
                        first_id = char.id
                        break
                if not npc_exists:
                    print('You do not have a character with this name. Please try again.')
                    continue
                is_first_valid = True
        # Get the second character
        print('Which character do you want to break a relationship with?')
        print('If you want to break the relationship with the player, just hit enter')
        list_of_char_ids = [rel[1] for rel in maker.relationships if rel[0] == first_id]
        list_of_char_names = [maker.characters[i].name.lower() for i in list_of_char_ids]
        print('Existing relationships: ' + str(list_of_char_names))
        second_name = ''
        second_id = 0
        is_second_valid = False
        while not is_second_valid:
            try:
                second_name = raw_input('>')
            except:
                second_name = input('>')
            if second_name == 'ret':
                return (False, 0)
            elif second_name == 'q':
                return (False, 1)
            else:
                if len(second_name) == 0:
                    # check if player is among the characters
                    if 'player' in list_of_char_names:
                        second_id = 0
                        second_name = 'Player'
                        is_second_valid = True
                    else:
                        print('Player is not among existing relationships. Try again')
                        continue
                else:
                    # Check if name exists
                    npc_found = False
                    for char in maker.characters.values():
                        if char.name.lower() == second_name.lower():
                            if char.id in list_of_char_ids:
                                second_id = char.id
                                npc_found = True
                                break
                    if not npc_found:
                        print('No such character exists in ' + first_name.lower() + '\'s relationships. Try again.')
                        continue
                    is_second_valid = True
        # find the index of the given relationship
        idx = 0
        rel_found = False
        for rel in maker.relationships:
            if rel[0] == first_id and rel[1] == second_id:
                rel_found = True
                break
            idx += 1
        if not rel_found:
            print('No such relationship exists. Please try again with different inputs.')
            return (False, 0)
        else:
            print('Relationship of ' + first_name.lower() + ' with ' + second_name.lower() + 'is removed successfully!')
            print('Keep in mind that relationships are non-symmetric, meaning the relationship of ' + second_name.lower() + ' with ' + first_name.lower() + ' is not deleted automatically if such relationship exists.')
            maker.relationships.pop(idx)
            return (True)  
    elif to_delete == 'e':
        # Delete item
        print('Please enter the name of the item you would like to delete.')
        print('Available items: ' + str([item.name for item in maker.items.values()]))
        item_name = ''
        item_id = 0
        is_item_valid = False
        while not is_item_valid:
            try:
                item_name = raw_input('>')
            except:
                item_name = input('>')
            if item_name == 'ret':
                return (False, 0)
            elif item_name == 'q':
                return (False, 1)
            else:
                # check if item exists
                item_found = False
                for i in maker.items.values():
                    if i.name.lower() == item_name.lower():
                        item_id = i.id
                        item_found = True
                        is_item_valid = True
                if not item_found:
                    print('No such item exists. Try again.')
                    continue
        # Check if there are any dependents on this item: inventory, action, precondition
        dependency_found = False
        # Check for inventory
        npc_name = ''
        for inv in maker.inventory:
            if inv[1] == item_id:
                dependency_found = True
                npc_name = maker.characters[inv[0]].name
                break
        if dependency_found:
            print('This item is added to ' + npc_name + '\'s inventory. You cannot delete ' + item_name + ' until this inventory condition is removed.')
            return (False, 0)
        # Check for precondition
        pre_name = ''
        pre_context = ''
        # possible preconditions: 'item_in_player_inventory', 'item_not_in_player_inventory', 'item_in_npc_inventory', 'item_in_location' 
        for (pre_id, pre) in maker.preconditions.items():
            for e in pre.elems:
                if type(e) is Item:
                    if e.id == item_id:
                        dependency_found = True
                        pre_name = pre.name
                        pre_context = pre.context
                        break
        if dependency_found:
            print('You have a ' + pre_context + ' precondition named ' + pre_name + ' that contains this item. You cannot delete ' + item_name + ' until this precondition is removed.')
            return (False, 0)
        # Check for action
        action_name = ''
        for action in maker.actions:
            if action[0] == 0:
                if action[1] == item_id:
                    dependency_found = True
                    action_name = action[2]
                    break
            if action[3] == 'ask for item':
                if action[6] == item_id:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'redeem item':
                if action[5] == item_id or action[6] == item_id:
                    dependency_found = True
                    action_name = action[2]
                    break
        if dependency_found:
            print('You have the action ' + action_name + " dependent on this item. You cannot delete " + item_name.lower() + ' until this action is removed.')
            return (False, 0)
        # At the point there are no dependents left
        print('Item ' + maker.items[item_id].name + ' is deleted successfully!')
        del maker.items[item_id]
        return (True)
    elif to_delete == 'f':
        print('Please enter the name of the character whose inventory you want to remove an item from.')
        print('If your character is the player, just hit enter')
        print('Available NPCs: ' + str([n.name for n in maker.characters.values() if n.name != 'Player']))
        char_name = ''
        char_id = 0
        is_char_valid = False
        while not is_char_valid:
            try:
                char_name = raw_input('>')
            except:
                char_name = input('>')
            if char_name == 'ret':
                return (False, 0)
            elif char_name == 'q':
                return (False, 1)
            else:
                if len(char_name) == 0:
                    # player - check if there is any inventory condition for player
                    cond_found = False
                    for inv in maker.inventory:
                        if inv[0] == 0:
                            cond_found = True
                            break
                    if cond_found:
                        char_name = 'Player'
                        char_id = 0
                        is_char_valid = True
                    else:
                        print('It looks like player does not have any items assigned for inventory. Please try again.')
                        continue
                else:
                    # check if character exists
                    char_found = False
                    for char in maker.characters.values():
                        if char.name.lower() == char_name.lower():
                            # Check if inventory condition exists for this character
                            char_found = True
                            cond_found = False
                            for inv in maker.inventory:
                                if inv[0] == char.id:
                                    cond_found = True
                                    char_name = char.name
                                    char_id = char.id
                                    break
                            if cond_found:
                                is_char_valid = True
                            else:
                                print('It looks like ' + char.name + ' does not have any items assigned for inventory. Please try again.')
                            break
                    if not char_found:
                        print('No such character exists. Please try again.')
                        continue
        # now get item
        print('Please enter the name of the item you would like to remove from ' + char_name + '\'s inventory.')
        list_of_inv_items = [maker.items[inv[1]].name for inv in maker.inventory if inv[0] == char_id]
        print('Items in inventory: ' + str(list_of_inv_items))
        item_name = ''
        item_id = 0
        is_item_valid = False
        while not is_item_valid:
            try:
                item_name = raw_input('>')
            except:
                item_name = input('>')
            if item_name == 'ret':
                return (False, 0)
            elif item_name == 'q':
                return (False, 1)
            else:
                # check if item exists and is actually in list_of_inv_items
                item_found = False
                for item in maker.items.values():
                    if item_name.lower() == item.name.lower():
                        item_found = True
                        item_in_inventory = False
                        for inv in list_of_inv_items:
                            if inv.lower() == item_name.lower():
                                item_in_inventory = True
                                item_id = item.id
                                break
                        if item_in_inventory:
                            is_item_valid = True
                        else:
                            print('This item is not in ' + char_name + '\'s inventory. Please try again.')
                        break
                if not item_found:
                    print('No such item exists. Please try again.')
                    continue
        # Inventory has no dependents - delete it
        idx = 0
        inv_found = False
        for inv in maker.inventory:
            if inv[0] == char_id and inv[1] == item_id:
                inv_found = True
                break
            idx += 1
        if not inv_found:
            print('No such inventory change exists. Please try again with different inputs.')
            return (False, 0)
        else:
            print(item_name + ' is removed from ' + char_name + '\'s inventory successfully!')
            maker.inventory.pop(idx)
            return (True) 
    elif to_delete == 'g':
        # Delete precondition
        print('Please enter the name of the precondition you would like to delete.')
        print('Keep in mind that you might have to delete its dependent plot points/actions/blocks/etc. first (if there are any).')
        print_preconditions(maker, [])
        pre_name = ''
        pre_id = 0
        is_pre_valid = False
        while not is_pre_valid:
            try:
                pre_name = raw_input('>')
            except:
                pre_name = input('>')
            if pre_name == 'ret':
                return (False, 0)
            elif pre_name == 'q':
                return (False, 1)
            else:
                # check if precondition exists
                pre_found = False
                for pre in maker.preconditions.values():
                    if pre.name.lower() == pre_name.lower():
                        pre_id = pre.id
                        pre_found = True
                        break
                if not pre_found:
                    print('No such precondition exists. Please try again.')
                    continue
                is_pre_valid = True
        # Check if there are any dependents
        dependency_found = False
        p1, p2 = 0, 0
        # Check for adjacency
        for adj in maker.adjacencies:
            if pre_id in adj[2]:
                dependency_found = True
                p1, p2 = adj[0], adj[1]
                break
        if dependency_found:
            print('This precondition is used as adjacency condition between the following plot points:')
            print(maker.plot_points[p1].name + ' -> ' + maker.plot_points[p2].name)
            print('You cannot delete this precondition until the adjacency is removed.')
            return (False, 0)
        # Check for blocks
        for block in maker.blocks:
            if pre_id in block[2]:
                dependency_found = True
                break
        if dependency_found:
            print('This precondition is used as a block condition between two locations. You cannot delete this precondition until the block is removed.')
            return (False, 0)
        # Check for actions
        action_name = ''
        for action in maker.actions:
            if action[3] == 'describe something':
                if pre_id in action[5]:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'call to location':
                if pre_id in action[8]:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'interaction with person':
                if pre_id in action[8]:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'ask for item':
                if pre_id in action[9]:
                    dependency_found = True
                    action_name = action[2]
                    break
            elif action[3] == 'redeem item':
                if pre_id in action[8]:
                    dependency_found = True
                    action_name = action[2]
                    break
        if dependency_found:
            print('This precondition is used for the action ' + action_name + '. You cannot delete this precondition until the action is removed.')
            return (False, 0)
        # No dependents left - delete the precondition
        print('Precondition ' + maker.preconditions[pre_id].name + ' is deleted successfully!')
        del maker.preconditions[pre_id]
        return (True)
    elif to_delete == 'h':
        pass
    elif to_delete == 'i':
        pass
    elif to_delete == 'j':
        pass
    elif to_delete == 'k':
        pass
    else:
        return (False, 0)

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
        # fields for objects
        self.blocks = []
        self.connections = []
        self.relationships = []
        self.inventory = []
        self.adjacencies = []
        self.actions = []

    def create_game(self):
        # First ask for player's starting location
        print('Which starting location do you want the player to start from?')
        print('Available locations: ' + str([loc.name for loc in self.locations.values()]))
        loc_name = ''
        player_loc = 0
        is_valid_location = False
        while not is_valid_location:
            try:
                loc_name = raw_input('>')
            except:
                loc_name = input('>')
            if loc_name == 'ret':
                return (False, 0)
            elif loc_name == 'q':
                return (False, 1)
            else:
                # Check if such location exists
                loc_found = False
                for loc in self.locations.values():
                    if loc.name.lower() == loc_name.lower():
                        player_loc = loc.id
                        loc_found = True
                        break
                if not loc_found:
                    print('No such location exists. Please try again.')
                    continue
                else:
                    is_valid_location = True
        # Now start writing in the game file
        f = open('game_file.txt', 'w')
        # Write the locations
        for (location_id, location) in self.locations.items():
            is_discovered = 0
            if location.isDiscovered:
                is_discovered = 1
            f.write('loc/' + str(location.name) + '/' + str(location.description) + '/' + str(is_discovered) + '\n')
        # Write the connections
        for connection in self.connections:
            f.write('con/' + str(connection[0]) + '/' + str(connection[1]) + '/' + connection[2] + '\n')
        # Write the items
        for (item_id, item) in self.items.items():
            is_gettable = 0
            if item.collectable:
                is_gettable = 1
            loc_id = -1
            if item.location:
                loc_id = item.location.id
            f.write('item/' + str(item.name) + '/' + str(item.description) + '/' + str(is_gettable) + '/' + str(item.examine) + '/' + str(loc_id) + '\n')
        # Write the player
        f.write('player/' + str(self.player.name) + '/' + str(player_loc) + '\n')
        # Write the npcs
        for (npc_id, npc) in self.characters.items():
            if npc.id == 0:
                continue
            npc_loc = -1
            if npc.curr_location:
                npc_loc = npc.curr_location.id
            f.write('npc/' + str(npc.name) + '/' + str(npc_loc) + '\n')
        # Write the relationships
        for rel in self.relationships:
            f.write('rel/' + str(rel[0]) + '/' + str(rel[1]) + '/' + str(rel[2]) + '/' + str(rel[3]) + '\n')
        # Write the inventory
        for i in self.inventory:
            f.write('inv/' + str(i[0]) + '/' + str(i[1]) + '\n')
        # Write the preconditions
        for (pre_id, pre) in self.preconditions.items():
            context = pre.context
            if context == 'item_in_player_inventory':
                f.write('pre/item_in_player_inventory/' + str(pre.elems[0]) + '\n')
            elif context == 'item_not_in_player_inventory':
                f.write('pre/item_not_in_player_inventory/' + str(pre.elems[0]) + '\n')
            elif context == 'item_in_npc_inventory':
                f.write('pre/item_in_npc_inventory/' + str(pre.elems[0]) + '/' + str(pre.elems[1]) + '\n')
            elif context == 'item_in_location':
                f.write('pre/item_in_location/' + str(pre.elems[0]) + '/' + str(pre.elems[1]) + '\n')
            elif context == 'player_is_friends_with':
                f.write('pre/player_is_friends_with/' + str(pre.elems[0]) + '\n')
            elif context == 'player_is_acquaintances_with':
                f.write('pre/player_is_acquaintances_with/' + str(pre.elems[0]) + '\n')
            elif context == 'player_dislikes':
                f.write('pre/player_dislikes/' + str(pre.elems[0]) + '\n')
            elif context == 'player_does_not_dislike':
                f.write('pre/player_does_not_dislike/' + str(pre.elems[0]) + '\n')
            elif context == 'player_in_location':
                f.write('pre/player_in_location/' + str(pre.elems[0]) + '\n')
            elif context == 'npc_in_location':
                f.write('pre/npc_in_location/' + str(pre.elems[0]) + '/' + str(pre.elems[1]) + '\n')
        # Write the blocks
        for block in self.blocks:
            txt = 'block/' + str(block[0]) + '/' + str(block[1]) + '/'
            for pre in block[2]:
                txt = txt + str(pre) + '-'
            txt = txt[:-1]
            txt += '\n'
            f.write(txt)
        # Write the plot points
        for (plot_id, plot) in self.plot_points:
            is_end = 0
            if plot.is_end:
                is_end = 1
            txt = 'plot/' + str(plot.name) + '/' + str(is_end) + '/' + str(plot.message)
            # Check if there are any changes
            for change in plot.changes_to_make:
                if change[0] == 'set_npc_location_none':
                    txt = txt + '/set_npc_location_none-' + str(change[1])
                elif change[0] == 'bring_npc_to':
                    txt = txt + '/bring_npc_to-' + str(change[1]) + '-' + str(change[2])
            txt += '\n'
            f.write(txt)
        # Write the adjacents
        for adj in self.adjacencies:
            txt = 'adj/' + str(adj[0]) + '/' + str(adj[1]) + '/'
            for pre in adj[2]:
                txt = txt + str(pre) + '-'
            txt = txt[:-1]
            txt += '\n'
            f.write(txt)
        # Write the actions
        for action in self.actions:
            txt = 'action/' + str(action[0]) + '/' + str(action[1]) + '/' + str(action[2]) + '/' + str(action[3]) + '/'
            if action[3] == 'describe something':
                txt = txt + str(action[4]) + '/'
                for pre in action[5]:
                    txt = txt + str(pre) + '-'
                txt = txt[:-1]
            elif action[3] == 'call to location':
                txt = txt + str(action[4]) + '/' + str(action[5]) + '/' + str(action[6]) + '/' + str(action[7]) + '/'
                for pre in action[8]:
                    txt = txt + str(pre) + '-'
                txt = txt[:-1]
            elif action[3] == 'interaction with person':
                txt = txt + str(action[4]) + '/' + str(action[5]) + '/' + str(action[6]) + '/' + str(action[7]) + '/'
                for pre in action[8]:
                    txt = txt + str(pre) + '-'
                txt = txt[:-1]
            elif action[3] == 'ask for item':
                txt = txt + str(action[4]) + '/' + str(action[5]) + '/' + str(action[6]) + '/' + str(action[7]) + '/' + str(action[8]) + '/'
                for pre in action[9]:
                    txt = txt + str(pre) + '-'
                txt = txt[:-1]
            elif action[3] == 'redeem item':
                txt = txt + str(action[4]) + '/' + str(action[5]) + '/' + str(action[6]) + '/' + str(action[7]) + '/'
                for pre in action[8]:
                    txt = txt + str(pre) + '-'
                txt = txt[:-1]
            txt += '\n'
            f.write(txt)
        # Writing complete
        print('Game file generated successfully.')
        f.close()

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
            is_gettable = result[3] == 'yes'
             # extract the location
            item_location = None
            if result[5] > -1:
                item_location = game_maker.locations[result[5]]
            # Create item
            new_item = Item(result[1], result[2], is_gettable, result[4], item_location)
            game_maker.items[new_item.id] = new_item
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
            # Add precondition
            result_category = result[2]
            elems = result[3:]
            new_precondition = Precondition(result_category, elems, result[1])
            game_maker.preconditions[new_precondition.id] = new_precondition
            print('Precondition added successfully!')
    elif entered.lower() == 'h':
        result = valid_plot_point(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            # extract is_end
            is_end = result[2] == 'yes'
            new_plot_point = PlotPoint(result[1], is_end, result[3], result[4])
            game_maker.plot_points[new_plot_point.id] = new_plot_point
            print('Plot point added successfully!')
    elif entered.lower() == 'i':
        result = valid_adjacency(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            game_maker.adjacencies.append((result[1], result[2], result[3]))
            print('Adjacency added successfully!')
    elif entered.lower() == 'j':
        result = valid_block(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            game_maker.blocks.append((result[1], result[2], result[3]))
            print('Block added successfully!')
    elif entered.lower() == 'k':
        result = valid_action(game_maker)
        if not result[0]:
            if result[1] == 1:
                print('Goodbye')
                break
        else:
            game_maker.actions.append(result[1:])
            print('Action added successfully!')
    elif entered.lower() == 'l':
        game_maker.create_game()
    elif entered.lower() == 'm':
        # Check added components
        print('Locations: ' + str([loc.name for loc in game_maker.locations.values()]))
        print('NPCs: ' + str([n.name for n in game_maker.characters.values()]))
        print('Items: ' + str([item.name for item in game_maker.items.values()]))
        print('Plot points: ' + str([plot.name for plot in game_maker.plot_points.values()]))
        print('Preconditions: ' + str([(pre.context, pre.name) for pre in game_maker.preconditions.values()]))
        print_connections(game_maker)
        print_relationships(game_maker)
    elif entered.lower() == 'n':
        result = valid_delete(game_maker)
        if type(result) is tuple:
            if not result[0]:
                if result[1] == 1:
                    print('Goodbye')
                    break
    else:
        print('Cannot process your request. Please pick an option from the menu.')