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

def menu_options():
    print('Options:')
    print('\ta) Add Location')
    print('\tb) Add NPC')
    print('\tc) Connect Locations')
    print('\td) Add Relationship')
    print('\te) Add Item to Inventory')
    print('\tg) Add Precondition')
    print('\th) Add Plot Point')
    print('\ti) Add Plot Point Adjacency')
    print('\tj) Add Block')
    print('\tk) Add Action')
    print('\tl) Submit Game')
    print('\tm) Check Added Components')

def valid_location(maker):
    # First get a valid location name
    print('Please enter the name of your location:')
    loc_name = ''
    is_loc_name_valid = False
    while not is_loc_name_valid:
        loc_name = raw_input('>')
        if len(loc_name) == 0:
            print('You cannot set an empty name. Please try again.')
            continue
        if loc_name == 'ret':
            return (False, 0)
        elif loc_name == 'q':
            return (False, 1)
        elif len(loc_name) < 2:
            print('Your location name cannot be less than 2 characters. Please try again.')
            continue
        else:
            same_name_found = False
            for (loc_id, loc) in maker.locations:
                if loc.name == loc_name:
                    same_name_found = True
                    print('You already added a location with the same name.')
                    break
            if not same_name_found:
                is_loc_name_valid = True
    # Now get a location description
    print('Please enter your location description:')
    loc_desc = ''
    is_loc_desc_valid = False
    while not is_loc_desc_valid:
        loc_desc = raw_input('>')
        if loc_desc == 'ret':
            return (False, 0)
        elif loc_desc == 'q':
            return (False, 1)
        is_loc_desc_valid = True
    # Now determine if your location should be marked as discovered
    print("Is your location discovered by default? Enter 'yes' or 'no':")
    loc_discovered = ''
    is_loc_discovered_valid = False
    while not is_loc_discovered_valid:
        loc_discovered = raw_input('>')
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

class GameMaker(object):

    def __init__(self):
        self.locations = {}
        self.characters = {}
        self.player = Player('') # initialize player
        self.characters[self.player.id] = self.player
        self.items = {}
        self.plot_points = {}
        self.preconditions = {}
        self.blocks = {}
        self.plot = None
    
    def add_component(self):
        pass

    def create_game(self):
        pass
    
    def check_validity(self):
        pass

# Start maker here
game_maker = GameMaker()
print('Welcome to Game Maker. You can create game components and make your own game file to play.')
print('Enter the required information to create your components. For multiple choice options, please enter the choice letter.')
print("Once you are done adding game components, enter 'l' to create your game file.")
print("If you would like to go back to main menu while creating a component, please enter 'ret'")
print('Press q anytime to quit the game maker.')
while True:
    menu_options()
    entered = raw_input('>')
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
        pass
    elif entered.lower() == 'c':
        pass
    elif entered.lower() == 'd':
        pass
    elif entered.lower() == 'e':
        pass
    elif entered.lower() == 'f':
        pass
    elif entered.lower() == 'g':
        pass
    elif entered.lower() == 'h':
        pass
    elif entered.lower() == 'i':
        pass
    elif entered.lower() == 'j':
        pass
    elif entered.lower() == 'k':
        pass
    elif entered.lower() == 'l':
        pass
    elif entered.lower() == 'm':
        # Check added components
        print('Locations: ' + str([loc.name for loc in game_maker.locations.values()]))
        print('Connections: ')
        print('NPCs: ' + str([n.name for n in game_maker.characters.values()]))
        print('Items: ' + str([item.name for item in game_maker.items.values()]))
        print('Plot:')
    else:
        print('Cannot process your request. Please pick an option from the menu.')