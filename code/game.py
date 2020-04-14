# Game

# Import classes
from gameState import GameState, PlotPoint, Plot
from dramaManager import DramaManager
from parser import Parser
from character import Character
from player import Player
from npc import NPC
from item import Item
from location import Location

# Import functions
from functions import *

class Game(object):

    # build game
    def __init__(self):
        self.build_game()
    
    def build_game(self):
        
        # Locations
        bedroom = Location("Bedroom", "You're standing in your small and cozy dorm bedroom.", True)
        hallway = Location("Hallway", "You're standing in the middle of the hallway in front of your door.\n There is a vending machine accross.", False)

        # Add connections
        bedroom.add_connection("out", hallway)
        hallway.add_connection("in", bedroom)

        # Items
        phone = Item("cell phone", "Iphone", True, "IphoneX", location=bedroom)

        vending_machine = Item("vending machine", "just a vending machine with snacks", False, "the variety of snacks is impressive.", location=hallway)
        snack = Item("snack", "delicious snack", False,"delicious snack", location=hallway)
        money = Item("Money", "money", True, "5 bucks", location=None)

        # Characters

        player = Player("", location=bedroom)
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
        ask_anna_money = PlotPoint("Can ask Anna for money")
        plot_graph.add_plot_point(ask_anna_money)
        go_back_to_bedroom = PlotPoint("Go back in to bedroom", changes_to_make=[('set_npc_location_none', anna)])
        plot_graph.add_plot_point(go_back_to_bedroom)
        player_in_bedroom = PlotPoint("Player in bedroom", changes_to_make=[('bring_npc_to', (brian, hallway))])
        plot_graph.add_plot_point(player_in_bedroom)
        brian_in_hallway = PlotPoint("Brian in hallway")
        plot_graph.add_plot_point(brian_in_hallway)
        ask_brian_money = PlotPoint("Can ask Brian for money")
        plot_graph.add_plot_point(ask_brian_money)
        buy_snack = PlotPoint("Can buy snack")
        plot_graph.add_plot_point(buy_snack)
        end_point = PlotPoint("END", is_end=True)
        plot_graph.add_plot_point(end_point)

        # Preconditions
        called_anna = ('npc_in_location', (anna, hallway))
        friendly_to_anna = ('player_is_friends_with', anna)
        rude_to_anna = ('player_dislikes', anna)
        in_bedroom = ('player_in_location', bedroom)
        brian_around = ('npc_in_location', (brian, hallway))
        talk_to_brian = ('player_is_friends_with', brian)
        have_money = ('item_in_player_inventory', money)
        not_have_money = ('item_not_in_player_inventory', money)
        have_snack = ('item_in_player_inventory', snack)
        
        # Set up the graph
        plot_graph.add_new_adjacent(plot_graph.start, anna_in_hallway, [called_anna])
        plot_graph.add_new_adjacent(anna_in_hallway, ask_anna_money, [friendly_to_anna])
        plot_graph.add_new_adjacent(ask_anna_money, buy_snack, [have_money])
        plot_graph.add_new_adjacent(anna_in_hallway, go_back_to_bedroom, [rude_to_anna, not_have_money])
        plot_graph.add_new_adjacent(go_back_to_bedroom, player_in_bedroom, [in_bedroom])
        plot_graph.add_new_adjacent(player_in_bedroom, brian_in_hallway, [brian_around])
        plot_graph.add_new_adjacent(brian_in_hallway, ask_brian_money, [talk_to_brian])
        plot_graph.add_new_adjacent(ask_brian_money, buy_snack, [have_money])
        plot_graph.add_new_adjacent(buy_snack, end_point, [have_snack])

        # Add actions
        phone.add_action('check social media', describe_something, ('You scroll through your feed but see nothing particularly iteresting.'))
        phone.add_action('call Anna', call_to_location, (hallway, anna, "You call Anna and ask if she would be down to meet up with you.\n" +\
                                                                         "'Of course! I will be in your hallway in a bit.' she responds.",
                                                                         "You already called Anna."))
        anna.add_action('friendly interaction', interaction_with_person, (player, anna, 20, "You compliment Anna's dress and tell a funny joke.\n" +\
                                                                                            "'Omg you're so funny!' she cries."),
                                                                                            preconditions=[('npc_in_location', (anna, hallway))])
        anna.add_action('rude interaction', interaction_with_person, (player, anna, -50, "You make fun of Anna's dress and make-up.\n" +\
                                                                                         "'You're such a prick! Ugh, I don't want to talk to you!' She yells and storms off the building."),
                                                                                         preconditions=[('npc_in_location', (anna, hallway))])
        anna.add_action('ask for money', ask_for_item, (player, anna, money, "You tell Anna that you need some money. She hands you 5 bucks.", "You already did this action."), 
                                                                                         preconditions=[('player_is_friends_with', anna), ('npc_in_location', (anna, hallway)), ('item_in_npc_inventory', (anna, money))])
        brian.add_action('get to know Brian', interaction_with_person, (player, brian, 50, "It turns out that you guys love pretty much the same stuff. He's like your brother from another mother!\n" +\
                                                                                           "Okay, that's a bit of exaggeration, but still he would help you with anything!"),
                                                                                        preconditions=[('npc_in_location', (brian, hallway))])
        brian.add_action('ask for money', ask_for_item, (player, brian, money, "You tell Brian that you're craving snacks. Before you even ask for money, he hands you 5 bucks. What a lad!", "You already did this action."), 
                                                                                         preconditions=[('player_is_friends_with', brian), ('npc_in_location', (brian, hallway)), ('item_in_npc_inventory', (brian, money))])
        vending_machine.add_action('buy a snack', redeem_item, (player, snack, money, "You buy a delicious snack from the vending machine."), preconditions=[have_money])

        # Initialize Game State
        npcs = {'anna': anna, 'brian': brian}
        locations = {'bedroom': bedroom, 'hallway': hallway}
        game_state = GameState(player, bedroom, plot_graph, npcs, locations)

        # Initialize the Drama Manager
        drama_manager = DramaManager(game_state)

        # Create parser
        self.parser = Parser(drama_manager)
    
    def describe_current_location(self):
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
    game = Game() # Create new game instance
    game.describe()
    prev_location = game.parser.drama_manager.game_state.current_location.name
    #game.parser.drama_manager.game_state.plot.print_plot()
    # Parse commands
    command = ""
    while not (command.lower() == "exit" or command.lower == "q"):
        if game.parser.drama_manager.game_state.current_location.name != prev_location:
            prev_location = game.parser.drama_manager.game_state.current_location.name
            game.describe()
        command = raw_input('>')
        result = game.parser.parse_command(command)
        if result:
            break
    print('Game ended')

game_loop()








        



