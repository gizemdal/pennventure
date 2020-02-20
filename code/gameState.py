# Game State
from character import Character

id = 0 # plot point id
class PlotPoint(object):

    def __init__(self):
        global id
        self.adjacents = {} # Dictionary of plotPoint -> dependencies/preconditions mapping
        self.id = id
        id += 1 # increment global id for unique ids per plot point

    def add_new_adjacent(self, plot_point, preconditions):
        if plot_point not in self.adjacents:
            self.adjacents[plot_point] = preconditions
    
    def add_precondition_to_existing_plot(self, plot_id, precondition):
        for plot_point in self.adjacents:
            if plot_point.id == plot_id:
                self.adjacents[plot_point].append(precondition)
                return
        print('No such adjacent plot point exists.')

# Plot data structure: a directed graph-like structure with plot points as vertices and plot dependencies as edges
class Plot(object):
    
    def __init__(self, start):
        self.start = start

class GameState(object):

    def __init__(self, player, start_at, start_plot):
        self.player = player
        self.current_location = start_at
        self.npcs = {}
        self.locations = {}
        self.start_plot = start_plot

    def is_condition_satisfied(self, condition):
        pass

