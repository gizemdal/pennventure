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
        money_anna = Item("Anna's money", "money", True, "5 bucks", location=None)
        money_brian = Item("Brian's money", "money", True, "5 bucks", location=None)

        # Characters

        player = Player("", location=bedroom)
        anna = NPC("Anna", location=None)
        brian = NPC("Brian", location=None)

        # Make player and Anna know each other
        player.acquaintances[anna.id] = (50, 10)
        anna.acquaintances[player.id] = (50, 18)

        anna.get_item(money_anna)
        brian.get_item(money_brian)

        # Plot graph
        plot_graph = Plot(PlotPoint("START"))
        anna_in_hallway = PlotPoint("Anna in hallway")
        plot_graph.add_plot_point(anna_in_hallway)
        ask_anna_money = PlotPoint("Can ask Anna for money")
        plot_graph.add_plot_point(ask_anna_money)
        go_back_to_bedroom = PlotPoint("Go back in to bedroom")
        plot_graph.add_plot_point(go_back_to_bedroom)
        brian_in_hallway = PlotPoint("Brian in hallway")
        plot_graph.add_plot_point(brian_in_hallway)
        ask_brian_money = PlotPoint("Can ask Brian for money")
        plot_graph.add_plot_point(ask_brian_money)
        buy_snack = PlotPoint("Can buy snack")
        plot_graph.add_plot_point(buy_snack)
        end_point = PlotPoint("END")
        plot_graph.add_plot_point(end_point)

        # Preconditions
        called_anna = ('npc_in_location', (anna, hallway))
        friendly_to_anna = ('player_is_friends_with', anna)
        rude_to_anna = ('player_is_acquaintances_with', anna)
        in_bedroom = ('player_in_location', bedroom)
        brian_around = ('npc_in_location', (brian, hallway))
        talk_to_brian = ('player_is_friends_with', brian)
        have_anna_money = ('item_in_player_inventory', money_anna)
        have_brian_money = ('item_in_player_inventory', money_brian)
        have_snack = ('item_in_player_inventory', snack)

        # Set up the graph
        plot_graph.add_new_adjacent(plot_graph.start, anna_in_hallway, [called_anna])
        plot_graph.add_new_adjacent(anna_in_hallway, ask_anna_money, [friendly_to_anna])
        plot_graph.add_new_adjacent(ask_anna_money, buy_snack, [have_anna_money])
        plot_graph.add_new_adjacent(anna_in_hallway, go_back_to_bedroom, [rude_to_anna])
        plot_graph.add_new_adjacent(go_back_to_bedroom, brian_in_hallway, [rude_to_anna, in_bedroom, brian_around])
        plot_graph.add_new_adjacent(brian_in_hallway, ask_brian_money, [talk_to_brian])
        plot_graph.add_new_adjacent(ask_brian_money, buy_snack, [have_brian_money])
        plot_graph.add_new_adjacent(buy_snack, end_point, [have_snack])

        # Print the plot graph
        #plot_graph.print_plot()

game = Game()







        



