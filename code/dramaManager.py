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
                    print(e)
                print('Items:')
                for i in player_location.items.keys():
                    print(i + ' : ' + player_location.items[i].description)
                print('People:')
                for p in player_location.characters.keys():
                    if p == self.game_state.player.name:
                        continue
                    print(p)
            # check if it's inventory
            elif action[0] == 'inventory':
                # Print out all the items and their descriptions in player's inventory
                print('Inventory:')
                for i in self.game_state.player.inventory.keys():
                    print(i + ' : ' + self.game_state.player.inventory[i].description)
        elif len(action) == 2:
            # check if it's direction
            if action[0] == 'direction':
                self.game_state.player.set_location(self.game_state.player.curr_location.connections[action[1]])
            elif action[0] == 'go to location':
                go_to_location = None
                for loc in self.game_state.locations.keys():
                    if action[1].lower() == loc:
                        go_to_location = self.game_state.locations[loc]
                        break
                if go_to_location:
                    self.game_state.player.set_location(go_to_location)
            elif action[0] == 'examine':
                pass # BURDAN DEVAM ET!!


        # Check if player made actions to move to next plot point
        # Conditions for plot points should be added such that no two plot points would be available at the same time
        for adj in self.game_state.plot.adjacency_list[self.game_state.current_plot_point.id]:
            all_conditions_satisfied = True
            for condition in adj[1]:
                result = self.game_state.is_condition_satisfied(condition)
                if not result:
                    all_conditions_satisfied = False
                    break
            if all_conditions_satisfied:
                self.game_state.current_plot_point = self.game_state.plot.plot_points[adj[0]]
                if self.game_state.current_plot_point.is_end:
                    game_end = True
                break
        return game_end
        
    