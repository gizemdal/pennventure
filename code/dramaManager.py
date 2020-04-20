# Drama Manager

from gameState import GameState

class DramaManager(object):

    def __init__(self, game_state):
        # Game state to manage
        self.game_state = game_state
    
    def update_game_state(self, action):
        game_end = False
        # Depending on the action update the game state and the current plot point
        # Figure out which action is going to be executed
        if len(action) == 1:
            # check if it's look around
            if action[0] == 'look around':
                player_location = self.game_state.player.curr_location
                # Print current location description, exits, items, people
                print(player_location.description)
                print('Exits:')
                for e in player_location.connections.keys():
                    print('\t' + e)
                print('Items:')
                for i in player_location.items.keys():
                    print('\t' + i + ' : ' + player_location.items[i].description)
                for i in self.game_state.player.inventory.keys():
                    print('\t' + i + ' : ' + self.game_state.player.inventory[i].description)
                if len(player_location.characters.keys()) > 1:
                    print('People:')
                    for p in player_location.characters.keys():
                        if player_location.characters[p].id == self.game_state.player.id:
                            continue
                        print('\t' + p)
            # check if it's inventory
            elif action[0] == 'inventory':
                # Print out all the items and their descriptions in player's inventory
                print('Inventory:')
                for i in self.game_state.player.inventory.keys():
                    print(i + ' : ' + self.game_state.player.inventory[i].description)
        elif len(action) == 2:
            # check if it's direction
            if action[0] == 'direction' and action[1] in self.game_state.player.curr_location.connections:
                # check if the direction is blocked
                if not self.game_state.player.curr_location.check_block(action[1], self.game_state):
                    self.game_state.player.set_location(self.game_state.player.curr_location.connections[action[1]])
                    self.game_state.current_location = self.game_state.player.curr_location
                else:
                    print('You cannot go in this direction. It is blocked.')
            elif action[0] == 'go to location':
                go_to_location = None
                for loc in self.game_state.locations.keys():
                    if action[1].lower() == self.game_state.locations[loc].name.lower():
                        go_to_location = self.game_state.locations[loc]
                        break
                if go_to_location:
                    self.game_state.player.set_location(go_to_location)
                    self.game_state.current_location = self.game_state.player.curr_location
            elif action[0] == 'examine':
                # check if the item to be examined is in the current location
                item_found = False
                if action[1].lower() in self.game_state.current_location.items.keys():
                    print(self.game_state.current_location.items[action[1].lower()].examine)
                    item_found = True
                if not item_found:
                    print("There is no such item here.")
            elif action[0] == 'take':
                # check if the item is in player inventory
                if action[1].lower() in self.game_state.player.inventory.keys():
                    print("You already took this item.")
                else:
                    # check if the item exists
                    item_found = False
                    if action[1].lower() in self.game_state.current_location.items.keys():
                        item_found = True
                    if not item_found:
                        print("There is no such item here.")
                    elif not self.game_state.current_location.items[action[1].lower()].collectable:
                        print("You can't take the " + action[1].lower())
                    else:
                        print("You take the " + action[1].lower())
                        self.game_state.player.get_item(self.game_state.current_location.items[action[1].lower()])
            elif action[0] == 'drop':
                # check if the item is in player inventory
                if action[1].lower() not in self.game_state.player.inventory.keys():
                    print("You don't have this item in your inventory.")
                else:
                    print("You drop the " + action[1].lower())
                    self.game_state.player.leave_item(action[1].lower())
            else:
                # special command
                if action[1].lower() == 'exit' or action[1].lower() == 'q':
                    return True
                command_found = False
                # First check if it's related to an inventory or location item
                for item in self.game_state.player.get_items_in_scope():
                    if action[1] in item.get_commands():
                        item.do_action(action[1], self.game_state)
                        command_found = True
                        break
                if not command_found:
                    # Check if it's related to a NPC character in the location
                    for npc in self.game_state.current_location.characters.keys():
                        if self.game_state.current_location.characters[npc].id == self.game_state.player.id:
                            continue
                        if action[1] in self.game_state.current_location.characters[npc].get_commands():
                            self.game_state.current_location.characters[npc].do_action(action[1], self.game_state)
                            command_found = True
                            break
                if not command_found:
                    print("I'm not sure what you want to do...")

        # Check if player made actions to move to next plot point
        # Conditions for plot points should be added such that no two plot points would be available at the same time
        for adj in self.game_state.plot.adjacency_list[self.game_state.current_plot_point.id]:
            all_conditions_satisfied = True
            for condition in adj[1]:
                result = self.game_state.is_condition_satisfied(condition)[0]
                if not result:
                    #print(condition)
                    all_conditions_satisfied = False
                    break
            if all_conditions_satisfied:
                self.game_state.current_plot_point = self.game_state.plot.plot_points[adj[0]]
                if len(self.game_state.current_plot_point.message) > 0:
                    print(self.game_state.current_plot_point.message)
                if self.game_state.current_plot_point.is_end:
                    game_end = True
                break

        # Make changes to the game if necessary
        self.make_changes(self.game_state.current_plot_point.changes)
        return game_end
    
    def make_changes(self, change_list):
        #print(self.game_state.current_plot_point.name)
        #print(change_list)
        # Possible list of changes:
        # Removing an npc from a location
        # Putting an npc into a location
        for change in change_list:
            if change[0] == 'set_npc_location_none':
                change[1].set_location(None)
            elif change[0] == 'bring_npc_to':
                change[1][0].set_location(change[1][1])
        
    