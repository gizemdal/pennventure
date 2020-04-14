# Game State
from character import Character
try:
    import queue
except ImportError:
    import Queue as queue

id = 0 # plot point id
class PlotPoint(object):

    def __init__(self, name, is_end=False, changes_to_make=[]):
        global id
        self.id = id
        self.name = name
        self.is_end = is_end # Is this plot point an end point?
        id += 1 # increment global id for unique ids per plot point
        self.changes = changes_to_make # list of actions drama manager should do if player reaches this plot point
    
    def __eq__(self, other):
        return self.id == other.id
    

# Plot data structure: a directed graph-like structure with plot points as vertices and plot dependencies as edges
class Plot(object):
    
    def __init__(self, start):
        self.start = start
        self.plot_points = {} # id -> plot point mapping
        self.adjacency_list = {} # plotPoint -> (adjacent plot point, dependencies/preconditions) mapping

        # add starting plot point to plot point dict
        self.plot_points[self.start.id] = self.start
    
    def add_plot_point(self, point):
        if point.id not in self.plot_points:
            self.plot_points[point.id] = point

    def add_new_adjacent(self, from_plot, to_plot, conditions):
        if from_plot.id not in self.adjacency_list:
            self.adjacency_list[from_plot.id] = [(to_plot.id, conditions)]
        else:
            self.adjacency_list[from_plot.id] = self.adjacency_list[from_plot.id] + [(to_plot.id, conditions)]
    
    def add_condition_to_existing_pair(self, from_plot, to_plot, condition):
        for adj in self.adjacency_list[from_plot.id]:
            if adj[0] == to_plot.id:
                adj = (adj[0], adj[1].append(condition))
                return
    
    def does_path_exist(self, from_plot, to_plot):
        q = queue.Queue()
        q.put(from_plot.id)
        visited = []
        while not q.empty():
            current = q.get()
            if self.adjacency_list[current]:
                for adj in self.adjacency_list[current]:
                    if adj[0] == to_plot.id:
                        return True
                    if adj[0] not in visited:
                        q.put(adj[0])
            visited.append(current)
        return False
    
    def print_plot(self):
        level = 0
        # explore the plot in a BFS way
        q = queue.Queue()
        q.put((self.start.id, level))
        visited = []
        while not q.empty():
            current = q.get()
            if current[0] in self.adjacency_list:
                for adj in self.adjacency_list[current[0]]:
                    if adj[0] not in visited:
                        q.put((adj[0], level + 1))
            visited.append(current[0])
            print('Name: ' + self.plot_points[current[0]].name + ', Id: ' + str(self.plot_points[current[0]].id) + ', Level: ' + str(current[1]))
            level += 1


class GameState(object):

    def __init__(self, player, start_at, plot, npcs={}, locations={}):
        self.player = player
        self.current_location = start_at
        self.npcs = npcs
        self.locations = locations
        self.plot = plot
        self.current_plot_point = self.plot.start

    def is_condition_satisfied(self, condition):
        # Condition = (condition text, condition element)
        # Depending on condition text, check if the given condition element satisfies the condition
        
        # Multiple if checks
        warning_text = ''
        if condition[0] == 'item_in_player_inventory':
            if self.player.check_item(condition[1]):
                return [True]
            else:
                warning_text = "You don't have the %s" % condition[1].name
        elif condition[0] == 'item_not_in_player_inventory':
            if condition[1].name not in self.player.inventory:
                return [True]
            else:
                warning_text = "You have the %s" % condition[1].name
        elif condition[0] == 'item_in_npc_inventory':
            # In this case, the condition[1] will be of type (npc, item) tuple
            npc = condition[1][0]
            if npc.check_item(condition[1][1]):
                return [True]
            else:
                warning_text = "%s doesn't have the %s" % (npc.name, condition[1][1].name)
        elif condition[0] == 'item_in_location':
            # In this case, the condition[1] will be of type (location, item) tuple
            loc = condition[1][0]
            if loc.check_item(condition[1][1]):
                return [True]
            else:
               warning_text = "%s isn't in the %s" % (condition[1][1].name, loc.name)
        elif condition[0] == 'player_is_friends_with':
            if condition[1].id in self.player.acquaintances:
                # In this case, the condition[1] will contain the NPC character
                if self.player.relationship_status(condition[1]) in ['friend', 'good friend']:
                    return [True]
            else:
               warning_text = "You're not close enough with %s to perform this action." % condition[1].name
        elif condition[0] == 'player_is_acquaintances_with':
            # In this case, the condition[1] will contain the NPC character
            if condition[1].id in self.player.acquaintances:
                return [True]
            else:
                warning_text = "You haven't met %s yet." % condition[1].name
        elif condition[0] == 'player_dislikes':
            # In this case, the condition[1] will contain the NPC character
            if condition[1].id in self.player.acquaintances:
                if self.player.relationship_status(condition[1]) == 'dislike':
                    return [True]
            else:
                warning_text = "You don't dislike %s enough to perform this action." % condition[1].name
        elif condition[0] == 'player_in_location':
            # In this case, the condition[1] will be a location
            if self.player.curr_location == condition[1]:
                return [True]
            else:
               warning_text = "You're not in the %s" % condition[1].name
        elif condition[0] == 'npc_in_location':
            # In this case, the condition[1] will be of type (npc, location) tuple
            npc = condition[1][0]
            if npc.curr_location == condition[1][1]:
                return [True]
            else:
                warning_text = "%s is not in the %s" % (npc.name, condition[1][1].name)
        return [False, warning_text]
