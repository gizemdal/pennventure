# Game
try:
    import tkinter
    from tkinter import *
except ImportError:
    from Tkinter import *
    import Tkinter as tkinter
# Import classes
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

class Game(object):

    # build game
    def __init__(self, player_name, game_file=""):
        if len(game_file) == 0:
            self.build_game(player_name)
        else:
            # Read from file
            locations = {}
            # add none entry
            locations[-1] = None
            npcs = {}
            items = {}
            plot_points = {}
            preconditions = {}
            player = None # overwrite later
            plot = None # overwrite later
            f = open(game_file, "r")
            for line in f:
                tokens = line.split('/')
                if tokens[0] == 'loc':
                    loc_name = tokens[1] # location name
                    loc_desc = tokens[2] # location description
                    is_discovered = bool(int(tokens[3][0]))
                    new_loc = Location(loc_name, loc_desc, is_discovered)
                    locations[new_loc.id] = new_loc
                elif tokens[0] == 'con':
                    # get first location
                    loc_from = locations[int(tokens[1])]
                    # get second location
                    loc_to = locations[int(tokens[2])]
                    loc_from.add_connection(tokens[3][:-1], loc_to)
                elif tokens[0] == 'item':
                    item_name = tokens[1] # name
                    item_desc = tokens[2] # description
                    item_ex = tokens[4] # examination
                    is_gettable = bool(int(tokens[3]))
                    start_loc = locations[int(tokens[5][:-1])] # starting location
                    new_item = Item(item_name, item_desc,is_gettable,item_ex,start_loc)
                    items[new_item.id] = new_item
                elif tokens[0] == 'player':
                    user_name = tokens[1]
                    if len(user_name) == 0:
                        user_name = player_name
                    player_loc = locations[int(tokens[2][:-1])]
                    player = Player(user_name, player_loc)
                elif tokens[0] == 'npc':
                    npc_name = tokens[1]
                    npc_loc = locations[int(tokens[2][:-1])]
                    new_npc = NPC(npc_name, npc_loc)
                    npcs[new_npc.id] = new_npc
                elif tokens[0] == 'rel':
                    if int(tokens[1]) == 0:
                        player.acquaintances[int(tokens[2])] = (int(tokens[3]), int(tokens[4][:-1]))
                    elif int(tokens[2]) == 0:
                        npcs[int(tokens[1])].acquaintances[0] = (int(tokens[3]), int(tokens[4][:-1]))
                    else:
                        npcs[int(tokens[1])].acquaintances[int(tokens[2])] = (int(tokens[3]), int(tokens[4][:-1]))
                elif tokens[0] == 'inv':
                    if int(tokens[1]) == 0:
                        player.get_item(items[int(tokens[2][:-1])])
                    else:
                        npc_inv = npcs[int(tokens[1])]
                        npc_inv.get_item(items[int(tokens[2][:-1])])
                elif tokens[0] == 'pre':
                    if tokens[1] == 'npc_in_location':
                        pre_npc = npcs[int(tokens[2])]
                        pre_loc = locations[int(tokens[3][:-1])]
                        new_pre = Precondition('npc_in_location',(pre_npc, pre_loc))
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'player_is_friends_with':
                        pre_npc = npcs[int(tokens[2][:-1])]
                        new_pre = Precondition('player_is_friends_with', pre_npc)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'player_dislikes':
                        pre_npc = npcs[int(tokens[2][:-1])]
                        new_pre = Precondition('player_dislikes', pre_npc)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'player_does_not_dislike':
                        pre_npc = npcs[int(tokens[2][:-1])]
                        new_pre = Precondition('player_does_not_dislike', pre_npc)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'player_in_location':
                        pre_loc = locations[int(tokens[2][:-1])]
                        new_pre = Precondition('player_in_location', pre_loc)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'item_in_player_inventory':
                        pre_item = items[int(tokens[2][:-1])]
                        new_pre = Precondition('item_in_player_inventory', pre_item)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'item_not_in_player_inventory':
                        pre_item = items[int(tokens[2][:-1])]
                        new_pre = Precondition('item_not_in_player_inventory', pre_item)
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'item_in_npc_inventory':
                        pre_npc = npcs[int(tokens[2])]
                        pre_item = items[int(tokens[3][:-1])]
                        new_pre = Precondition('item_in_npc_inventory', (pre_npc, pre_item))
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'item_in_location':
                        pre_loc = locations[int(tokens[2])]
                        pre_item = items[int(tokens[3][:-1])]
                        new_pre = Precondition('item_in_location', (pre_loc, pre_item))
                        preconditions[new_pre.id] = new_pre
                    elif tokens[1] == 'player_is_acquaintances_with':
                        pre_npc = npcs[int(tokens[2][:-1])]
                        new_pre = Precondition('player_is_acquaintances_with', pre_npc)
                        preconditions[new_pre.id] = new_pre
                elif tokens[0] == 'block':
                    # get first location
                    loc_from = locations[int(tokens[1])]
                    direction = tokens[2]
                    split_conditions = tokens[3].split('-')
                    for condition in split_conditions:
                        if condition[-1] != '\n':
                            loc_from.add_block(direction, preconditions[int(condition)])
                        else:
                            loc_from.add_block(direction, preconditions[int(condition[:-1])])
                elif tokens[0] == 'plot':
                    plot_name = tokens[1]
                    is_end = False
                    changes_to_make = []
                    if len(tokens) > 3:
                        is_end = bool(int(tokens[2]))
                        for i in range (3, len(tokens)):
                            split_changes = tokens[i].split('-')
                            if split_changes[0] == 'set_npc_location_none':
                                if split_changes[1][-1] != '\n':
                                    changes_to_make.append(('set_npc_location_none', npcs[int(split_changes[1])]))
                                else:
                                    changes_to_make.append(('set_npc_location_none', npcs[int(split_changes[1][:-1])]))
                            elif split_changes[0] == 'bring_npc_to':
                                if split_changes[2][-1] != '\n':
                                    changes_to_make.append(('bring_npc_to', (npcs[int(split_changes[1])], locations[int(split_changes[2])])))
                                else:
                                    changes_to_make.append(('bring_npc_to', (npcs[int(split_changes[1])], locations[int(split_changes[2][:-1])])))
                    else:
                        is_end = bool(int(tokens[2][:-1]))
                    new_plot_point = PlotPoint(plot_name, is_end, changes_to_make)
                    plot_points[new_plot_point.id] = new_plot_point
                    if new_plot_point.id == 0:
                        # This is the START point
                        plot = Plot(new_plot_point)
                    else:
                        plot.add_plot_point(new_plot_point)
                elif tokens[0] == 'adj':
                    from_point = plot_points[int(tokens[1])]
                    to_point = plot_points[int(tokens[2])]
                    conditions = []
                    split_conditions = tokens[3].split('-')
                    for condition in split_conditions:
                        if condition[-1] == '\n':
                            conditions.append(preconditions[int(condition[:-1])])
                        else:
                            conditions.append(preconditions[int(condition)])
                    plot.add_new_adjacent(from_point, to_point, conditions)
                elif tokens[0] == 'action':
                    subject = None
                    if int(tokens[1]) == 0:
                        # binded to item
                        subject = items[int(tokens[2])]
                    elif int(tokens[1]) == 1:
                        # binded to npc
                        subject = npcs[int(tokens[2])]
                    else:
                        continue
                    action_name = tokens[3]
                    if tokens[4] == 'describe something':
                        action_desc = tokens[5][:-1]
                        subject.add_action(action_name, describe_something, (action_desc))
                    elif tokens[4] == 'call to location':
                        action_loc = locations[int(tokens[5])]
                        action_npc = npcs[int(tokens[6])]
                        action_desc = tokens[7]
                        action_repeated = tokens[8]
                        conditions = []
                        # extract preconditions
                        split_conditions = tokens[9].split('-')
                        for condition in split_conditions:
                            if condition[-1] == '\n':
                                conditions.append(preconditions[int(condition[:-1])])
                            else:
                                conditions.append(preconditions[int(condition)])
                        subject.add_action(action_name, call_to_location, (action_loc, action_npc, action_desc, action_repeated), preconditions=conditions)
                    elif tokens[4] == 'interaction with person':
                        person_one = None
                        person_two = None
                        if int(tokens[5]) == 0:
                            person_one = player
                            person_two = npcs[int(tokens[6])]
                        elif int(tokens[6]) == 0:
                            person_one = npcs[int(tokens[5])]
                            person_two = player
                        else:
                            person_one = npcs[int(tokens[5])]
                            person_two = npcs[int(tokens[6])]
                        interaction_score = int(tokens[7])
                        action_desc = tokens[8]
                        conditions = []
                        # extract preconditions
                        split_conditions = tokens[9].split('-')
                        for condition in split_conditions:
                            if condition[-1] == '\n':
                                conditions.append(preconditions[int(condition[:-1])])
                            else:
                                conditions.append(preconditions[int(condition)])
                        subject.add_action(action_name, interaction_with_person, (person_one, person_two, interaction_score, action_desc), preconditions=conditions)
                    elif tokens[4] == 'ask for item':
                        person_one = None
                        person_two = None
                        if int(tokens[5]) == 0:
                            person_one = player
                            person_two = npcs[int(tokens[6])]
                        elif int(tokens[6]) == 0:
                            person_one = npcs[int(tokens[5])]
                            person_two = player
                        else:
                            person_one = npcs[int(tokens[5])]
                            person_two = npcs[int(tokens[6])]
                        action_item = items[int(tokens[7])]
                        action_desc = tokens[8]
                        action_repeated = tokens[9]
                        conditions = []
                        # extract preconditions
                        split_conditions = tokens[10].split('-')
                        for condition in split_conditions:
                            if condition[-1] == '\n':
                                conditions.append(preconditions[int(condition[:-1])])
                            else:
                                conditions.append(preconditions[int(condition)])
                        subject.add_action(action_name, ask_for_item, (person_one, person_two, action_item, action_desc, action_repeated), preconditions=conditions)
                    elif tokens[4] == 'redeem item':
                        person = None
                        if int(tokens[5]) == 0:
                            person = player
                        else:
                            person = npcs[int(tokens[5])]
                        buy_item = items[int(tokens[6])]
                        use_item = items[int(tokens[7])]
                        action_desc = tokens[8]
                        conditions = []
                        # extract preconditions
                        split_conditions = tokens[9].split('-')
                        for condition in split_conditions:
                            if condition[-1] == '\n':
                                conditions.append(preconditions[int(condition[:-1])])
                            else:
                                conditions.append(preconditions[int(condition)])
                        subject.add_action(action_name, redeem_item, (person, buy_item, use_item, action_desc), preconditions=conditions)
            # Now create the game state
            game_state = GameState(player, plot, npc_dict=npcs, location_dict=locations)
            drama_manager = DramaManager(game_state)
            self.parser = Parser(drama_manager)
    def build_game(self, player_name):
        
        # Locations
        bedroom = Location("Bedroom", "You're standing in your small and cozy dorm bedroom.", True)
        hallway = Location("Hallway", "You're standing in the middle of the hallway in front of your door.\n There is a vending machine accross.", False)

        # Add connections
        bedroom.add_connection("out", hallway)
        #hallway.add_connection("in", bedroom)

        # Items
        phone = Item("cell phone", "Iphone", True, "IphoneX", location=bedroom)

        vending_machine = Item("vending machine", "just a vending machine with snacks", False, "the variety of snacks is impressive.", location=hallway)
        snack = Item("snack", "delicious snack", False,"delicious snack", location=hallway)
        money = Item("Money", "money", True, "5 bucks", location=None)
        key = Item("Key", 'key', True, 'Door key', location=bedroom)

        # Characters

        player = Player(player_name, location=bedroom)
        anna = NPC("Anna", location=None)
        brian = NPC("Brian", location=None)

        # Make player and Anna know each other
        player.acquaintances[anna.id] = (40, 10)
        anna.acquaintances[player.id] = (40, 18)

        # Put money in Anna and Brian's inventory
        anna.get_item(money)
        brian.get_item(money)

        # Plot graph
        plot_graph = Plot(PlotPoint("START"))
        anna_in_hallway = PlotPoint("Anna in hallway")
        plot_graph.add_plot_point(anna_in_hallway)
        go_back_to_bedroom = PlotPoint("Go back in to bedroom", changes_to_make=[('set_npc_location_none', anna)])
        plot_graph.add_plot_point(go_back_to_bedroom)
        player_in_bedroom = PlotPoint("Player in bedroom", changes_to_make=[('bring_npc_to', (brian, hallway))])
        plot_graph.add_plot_point(player_in_bedroom)
        brian_in_hallway = PlotPoint("Brian in hallway")
        plot_graph.add_plot_point(brian_in_hallway)
        buy_snack = PlotPoint("Can buy snack", changes_to_make=[('set_npc_location_none', brian), ('set_npc_location_none', anna)])
        plot_graph.add_plot_point(buy_snack)
        end_point = PlotPoint("END", is_end=True)
        plot_graph.add_plot_point(end_point)

        # Preconditions
        called_anna = Precondition('npc_in_location', (anna, hallway))
        friendly_to_anna = Precondition('player_is_friends_with', anna)
        rude_to_anna = Precondition('player_dislikes', anna)
        can_call_anna = Precondition('player_does_not_dislike', anna)
        in_bedroom = Precondition('player_in_location', bedroom)
        player_has_key = Precondition('item_in_player_inventory', key)
        brian_around = Precondition('npc_in_location', (brian, hallway))
        talk_to_brian = Precondition('player_is_friends_with', brian)
        have_money = Precondition('item_in_player_inventory', money)
        not_have_money = Precondition('item_not_in_player_inventory', money)
        have_snack = Precondition('item_in_player_inventory', snack)
        anna_have_money = Precondition('item_in_npc_inventory', (anna, money))
        brian_have_money = Precondition('item_in_npc_inventory', (brian, money))

        # Set up blocks
        bedroom.add_block('out', player_has_key)
        
        # Set up the graph
        plot_graph.add_new_adjacent(plot_graph.start, anna_in_hallway, [called_anna])
        plot_graph.add_new_adjacent(anna_in_hallway, buy_snack, [friendly_to_anna, have_money])
        plot_graph.add_new_adjacent(anna_in_hallway, go_back_to_bedroom, [rude_to_anna, not_have_money])
        plot_graph.add_new_adjacent(go_back_to_bedroom, player_in_bedroom, [in_bedroom])
        plot_graph.add_new_adjacent(player_in_bedroom, brian_in_hallway, [brian_around])
        plot_graph.add_new_adjacent(brian_in_hallway, buy_snack, [talk_to_brian, have_money])
        plot_graph.add_new_adjacent(buy_snack, end_point, [have_snack])

        # Add actions
        phone.add_action('check social media', describe_something, ('You scroll through your feed but see nothing particularly iteresting.'))
        phone.add_action('call Anna', call_to_location, (hallway, anna, "You call Anna and ask if she would be down to meet up with you.\n" +\
                                                                         "'Of course! I will be in your hallway in a bit.' she responds.",
                                                                         "You already called Anna."), preconditions=[can_call_anna])
        anna.add_action('friendly interaction', interaction_with_person, (player, anna, 20, "You compliment Anna's dress and tell a funny joke.\n" +\
                                                                                            "'Omg you're so funny!' she cries."),
                                                                                            preconditions=[called_anna])
        anna.add_action('rude interaction', interaction_with_person, (player, anna, -999, "You make fun of Anna's dress and make-up.\n" +\
                                                                                         "'You're such a prick! Ugh, I don't want to talk to you!' She yells and storms off the building."),
                                                                                         preconditions=[called_anna])
        anna.add_action('ask for money', ask_for_item, (player, anna, money, "You tell Anna that you need some money. She hands you 5 bucks.", "You already did this action."), 
                                                                                         preconditions=[friendly_to_anna, called_anna, anna_have_money])
        brian.add_action('get to know Brian', interaction_with_person, (player, brian, 50, "It turns out that you guys love pretty much the same stuff. He's like your brother from another mother!\n" +\
                                                                                           "Okay, that's a bit of exaggeration, but still he would help you with anything!"),
                                                                                        preconditions=[brian_around])
        brian.add_action('ask for money', ask_for_item, (player, brian, money, "You tell Brian that you're craving snacks. Before you even ask for money, he hands you 5 bucks. What a lad!", "You already did this action."), 
                                                                                         preconditions=[talk_to_brian, brian_around, brian_have_money])
        vending_machine.add_action('buy a snack', redeem_item, (player, snack, money, "You buy a delicious snack from the vending machine."), preconditions=[have_money])

        # Initialize Game State
        npcs = {anna.id: anna, brian.id: brian}
        locations = {bedroom.id: bedroom, hallway.id: hallway}
        game_state = GameState(player, plot_graph, npcs, locations)

        # Initialize the Drama Manager
        drama_manager = DramaManager(game_state)

        # Create parser
        self.parser = Parser(drama_manager)
    
    def describe_current_location(self):
        print(str(self.parser.drama_manager.game_state.player.curr_location.name) + ':')
        print(self.parser.drama_manager.game_state.player.curr_location.description)
        
    def describe_exits(self):
        # This method lists the directions that the player can take to exit from current location
        exits = []
        for exit in self.parser.drama_manager.game_state.player.curr_location.connections.keys():
            exits.append(exit.capitalize())
        print('Exits:')
        for e in exits:
            print('\t' + e)
            
    def describe_items(self):
        # This method describes the items in current location
        if len(self.parser.drama_manager.game_state.player.curr_location.items) > 0:
            print('You see: ')
            for item_name in self.parser.drama_manager.game_state.player.curr_location.items:
                item = self.parser.drama_manager.game_state.player.curr_location.items[item_name]
                print('\t' + item.name + ' : ' + item.description)
                special_commands = item.get_commands()
                for cmd in special_commands:
                    print('\t\t' + cmd)
            if self.parser.drama_manager.game_state.player.inventory:
                print('You have: ')
                for item_name, i in self.parser.drama_manager.game_state.player.inventory.items():
                    print('\t' + i.name + ' : ' + i.description)
                    special_commands = i.get_commands()
                    for cmd in special_commands:
                        print('\t\t' + cmd)
    
    def describe_people(self):
        # This method describes the characters in current location
        if len(self.parser.drama_manager.game_state.player.curr_location.characters) > 1:
            print('People:')
            for person_name in self.parser.drama_manager.game_state.player.curr_location.characters:
                person = self.parser.drama_manager.game_state.player.curr_location.characters[person_name]
                if person.id == self.parser.drama_manager.game_state.player.id:
                    continue
                print('\t' + person_name)
                special_commands = person.get_commands()
                for cmd in special_commands:
                    print('\t\t' + cmd)

    
    def describe(self):
        self.describe_current_location()
        self.describe_exits()
        self.describe_items()
        self.describe_people()

def game_loop():
    print('Welcome to Pennventure! You will be trying to solve a puzzle provided.')
    print('Would you like to play the default game or upload a game file? Enter Default for default, otherwise enter whatever you wish.')
    default_or_upload = ''
    try:
        default_or_upload = raw_input('>')
    except:
        default_or_upload = input('>')
    file_name = ''
    if default_or_upload.lower() != 'default':
        print('Please enter the name of the file you would like to upload. Do not forget the file name extension!')
        try:
            file_name = raw_input('>')
        except:
            file_name = input('>')
    print('Awesome, let us start the game! You will be trying to solve a puzzle provided. First, let us start by getting your name.')
    player_name = ''
    try:
        player_name = raw_input('Your name: ')
    except:
        player_name = input('Your name: ')
    print('Hello ' + player_name + '! Let us begin our adventure...')
    game = Game(player_name, game_file=file_name) # Create new game instance
    game.describe()
    prev_location = game.parser.drama_manager.game_state.current_location.name
    # Parse commands
    command = ""
    while not (command.lower() == "exit" or command.lower == "q"):
        if game.parser.drama_manager.game_state.current_location.name != prev_location:
            prev_location = game.parser.drama_manager.game_state.current_location.name
            game.describe()
        try:
            command = raw_input('>')
        except:
            command = input('>')
        result = game.parser.parse_command(command)
        if result:
            break
    print('Game ended')

#Run game loop
game_loop()
#game = Game('example.txt')






        



