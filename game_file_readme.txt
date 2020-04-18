Game File Description:

- Id values of -1 means type is None
- Always create the starting location first (thus start location will have id of 0)
- Always create the player first (thus player will always have character id of 0)
- Always create the start plot point first (thus start will always have plot point id of 0)

loc (location) -> location name/location description/is discovered? (1 = True, 0 = False)
con (connection) -> from location id/to location id/direction name
item (item) -> item name/item description/item examine text/gettable (1 = True, 0 = False)/location id
player (player character) -> player name/start location id
npc (npc character) -> npc name/-1
rel (relationship) -> from char id/to char id/short term score/long term score
inv (inventory) -> character id/item id
pre (preconditions) -> precondition name/necessary ids
block (block) -> from location/direction/list of precondition ids
plot (plot point) -> plot point name/is end? (1 = True, 0 = False)/list of changes to make (change_category-required_ids)
adj (adjacency) -> from plot point id/to plot point id/precondition ids list
action (special command) -> is item or npc (0 = item, 1 = npc)/item or npc id/command name/function name/arguments