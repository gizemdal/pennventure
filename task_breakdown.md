### CIS497 Task Breakdown:

My senior design project consists of both a text-adventure game engine and a game maker (both with command-line interface). I was inspired by CIS700 (Interactive Fiction & Text Generation) taught by CCB for this project. Here is a breakdown of all the components of my project and an indicator of which component belongs to which class (CIS 700/497):

- Item, Location, Parser, special functions, location connections, blocks

My implementation for Item, Location and Parser classes follows our text adventure game implementation from CIS700. I also used the same format for special function structures, adding actions to items/npcs, adding connections and blocks to locations. However, there are some differences between the class structures and object fields.

- Character (NPC and Player), Precondition

CIS700 introduces characters and preconditions in the game, however all the characters are considered as 'items' and preconditions aren't objects. For CIS497, I made characters into their own class and added capabilities such as relationship formation, adding/leaving items, leaving/visiting locations that are not present in the game I had built for CIS700. The preconditions I have built for CIS497 are also very different in structure compared to those in CIS700 and have different categories such as friendship precondition, npc inventory, etc.

- Drama Manager

Drama manager is a game component I built solely for CIS497. I was inspired by several research papers focused on interactive fiction where the drama manager approach is common. The drama manager updates the game state and makes the player progress in the plot.

- Game State

My game state component for CIS497 is somewhat similar to the Game component in CIS700. However, the game state for CIS497 has different capabilities compared to the one in CIS700. The game state I built for CIS497 has all the information regarding the player, all the NPC characters, all the locations and the plot graph.

- Plot Graph & Plot Points

This component is made solely for CIS497. A plot graph is a directed graph of plot points and preconditions attached to each edge. Every plot point also contains a list of changes to alter in the game state if that plot point is reached.

- Game File Reader

This component is made solely for CIS497. A game file reader takes in a filename as input and builds the game with all of its components.

- Game Maker

This component is made solely for CIS497. The game maker is a separate application that allows users to create their own games and export them as game files. These game files can be uploaded to the game component to be read by the Game File Reader and be played.