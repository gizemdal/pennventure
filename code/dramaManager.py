# Drama Manager

from gameState import GameState

class DramaManager(object):

    def __init__(self, game_state):
        # Game state to manage
        self.game_state = game_state
    
    def update_game_state(self, action):
        game_end = False
        # Depending on the action update the game state and the current plot point
        # Example:
        # write code for updating game state here

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
        
    