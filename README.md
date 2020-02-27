# senior_design
My text adventure game for Senior Capstone Project

Game: the main class where all the necessary game data is built. Contains parser reference

Parser: class responsible of taking in player commands, determining the type of command (direction, action, etc.) and making necessary function calls for game_state. Contains drama manager reference

Drama Manager: class responsible for the plot direction and introducing characters/items to the game depending on the plot point the player is at. Updates the current plot of the game after getting command feedback from parser and manages the game state. Contains game state reference

Game State: Contains all the data from the game (player, npcs, locations, plot graph, etc.) Has a function 'is_condition_satisfied' that can check if a given condition is satisfied in the game yet. Contains references to the player, npcs, items, locations, the plot graph of the game, etc.

Plot: A directed graph data structure where vertices are PlotPoint objects and edges are conditions that need to be satisfied in order to move to the next plot point. There must exist a directed path between two plot points for one plot point to be reachable from the other.

Character: Parent class that represents characters in the game. Each character has a name, current location, inventory, acquaintances dictionary and an id (useful for dictionary query)

Player: Inherits from Character. Represents the player in the game

NPC: Inherits from Character. Represents NPC characters in the game. Every NPC instance contains a list of actions that the player can perform with them

Location: Represents locations in the game. Each location has a name, description, connected locations, items present in location, characters present in location, blocks that prevent player to go to adjacent locations unless some puzzles are solved

Item: Represents items in the game. Items can be divided into two categories: collectable and non-collectable. An item has a name, description and current location. Every Item instance contains a list of actions that the player can perform with them

Functions.py: This file contains special functions associated with items/npcs
