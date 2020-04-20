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
        return (True, 'player_in_location', loc_id)
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
        return (True, 'npc_in_location', npc_id, loc_id)
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
        return (True, 'item_in_player_inventory', item_id)
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
        return (True, 'item_in_npc_inventory', npc_id, item_id)
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
        return (True, 'item_not_in_player_inventory', item_id)
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
        return (True, 'item_in_location', loc_id, item_id)
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
            return (True, 'player_is_friends_with', npc_id)
        elif category == 'h':
            return (True, 'player_is_acquaintances_with', npc_id)
        elif category == 'i':
            return (True, 'player_dislikes', npc_id)
        elif category == 'j':
            return (True, 'player_does_not_dislike', npc_id)
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
                # Check if a character with given name already exists
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
                            changes.append(('bring_npc_to', info_2[1], info_2[2]))
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
    print('Available plot points: ' + str([plot.name for plot in game_maker.plot_points.values()]))
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
    print('Available plot points: ' + str([plot.name for plot in game_maker.plot_points.values() if plot.name.lower() != from_plot.lower()]))
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
    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values()]))
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
                print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
            else:
                # Check if this precondition was already added
                if pre_id in preconditions:
                    print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                    print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
                else:
                    preconditions.append(pre_id)
                    print('Precondition added successfully!')
                    print('Please enter the name of the preconditions you would like to attach to this graph edge one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
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
    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values()]))
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
                print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
            else:
                # Check if this precondition was already added
                if pre_id in preconditions:
                    print('You already added this precondition. Please pick another one or just hit Enter if you are done.')
                    print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
                else:
                    preconditions.append(pre_id)
                    print('Precondition added successfully!')
                    print('Please enter the names of the preconditions you would like to attach to this block one at a time.')
                    print('If you are done adding preconditions, just hit Enter.')
                    print('Available preconditions: ' + str([pre.name for pre in maker.preconditions.values() if pre.id not in preconditions]))
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
        return (True, subject, subject_id, command_name, 'describe something', description)
    elif action == 'b':
        # Call NPC to Location
        pass
    elif action == 'c':
        # Interact with Person
        pass
    elif action == 'd':
        # Ask for Item
        pass
    elif action == 'e':
        # Redeem Item
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
            result_category = result[1]
            elems = result[2:]
            new_precondition = Precondition(result_category, elems)
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
        print('This option is not implemented yet.')
    elif entered.lower() == 'l':
        # ASK FOR PLAYER START LOCATION
        print('This option is not implemented yet.')
    elif entered.lower() == 'm':
        # Check added components
        # PUT THIS ALL IN ANOTHER FUNCTION
        print('Locations: ' + str([loc.name for loc in game_maker.locations.values()]))
        print('NPCs: ' + str([n.name for n in game_maker.characters.values()]))
        print('Items: ' + str([item.name for item in game_maker.items.values()]))
        print('Plot points: ' + str([plot.name for plot in game_maker.plot_points.values()]))
        print('Preconditions: ' + str([pre.name for pre in game_maker.preconditions.values()]))
    elif entered.lower() == 'n':
        print('This option is not implemented yet.')
    else:
        print('Cannot process your request. Please pick an option from the menu.')