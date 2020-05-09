# Pennventure: Interactive Fiction Game Simulator & Maker

### List of default game simulator commands
- look around: prints a description of everything around the player
- inventory: prints a list of items in player's inventory
- take (item): puts the entered item in player's inventory if the item is gettable and in the same location as the player
- drop (item): removes the entered item from player's inventory and places it in the current location
- examine (item): prints the examine text of the entered item
- go (direction): moves the player to the next location in given direction (if such connection exists and it is not blocked)
- exit/q: quit the game

### Directions
- north (n)
- south (s)
- east (e)
- west (w)
- in
- out

### How to run
- For game maker, run gameMaker.py
- To play the game, run game.py

### Game Simulator classes and their functionality

- Game: the main class where all the necessary game data is built. Contains parser reference

- Parser: class responsible of taking in player commands, determining the type of command (direction, action, etc.) and making necessary function calls for game_state. Contains drama manager reference

- Drama Manager: class responsible for the plot direction and introducing characters/items to the game depending on the plot point the player is at. Updates the current plot of the game after getting command feedback from parser and manages the game state. Contains game state reference

- Game State: Contains all the data from the game (player, npcs, locations, plot graph, etc.) Has a function 'is_condition_satisfied' that can check if a given condition is satisfied in the game yet. Contains references to the player, npcs, items, locations, the plot graph of the game, etc.

- Plot: A directed graph data structure where vertices are PlotPoint objects and edges are conditions that need to be satisfied in order to move to the next plot point. There must exist a directed path between two plot points for one plot point to be reachable from the other.

- Character: Parent class that represents characters in the game. Each character has a name, current location, inventory, acquaintances dictionary and an id (useful for dictionary query)

- Player: Inherits from Character. Represents the player in the game

- NPC: Inherits from Character. Represents NPC characters in the game. Every NPC instance contains a list of actions that the player can perform with them

- Location: Represents locations in the game. Each location has a name, description, connected locations, items present in location, characters present in location, blocks that prevent player to go to adjacent locations unless some puzzles are solved

- Item: Represents items in the game. Items can be divided into two categories: collectable and non-collectable. An item has a name, description and current location. Every Item instance contains a list of actions that the player can perform with them

- Functions.py: This file contains special functions associated with items/npcs

### Demo Videos

- Gameplay demo: https://vimeo.com/409916978
- Game maker demo: https://vimeo.com/409922468
- Final edits demo: https://vimeo.com/416420576
