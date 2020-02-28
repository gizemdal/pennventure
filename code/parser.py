# Parser
import string
from gameState import GameState
from dramaManager import DramaManager

def tokenize(text):
    tokens = []
    words = text.split(' ')
    for word in words:
        if len(word) == 0:
            continue
        w = []
        for c in word:
            if c in string.punctuation:
                if len(w) != 0:
                    tokens.append(''.join(w))
                    w = []
                tokens.append(c)
            else:
                if c not in string.whitespace:
                    w.append(c)
        if len(w) != 0:
            tokens.append(''.join(w))
    return tokens

class Parser(object):

    def __init__(self, drama):
        # A pointer to the drama manager, which has a pointer to the game state
        self.drama_manager = drama
        # A list of all of the commands that the player has issued.
        self.command_history = []
    
    def parse_command(self, command):
        # TODO: Finish implementation
        result = self.categorize_command(command)

        # pass result to drama manager
        game_end = self.drama_manager.update_game_state(result)
        return game_end
    
    def categorize_command(self, command):
        # Determine which category the command belongs to
        # TODO: Implement this

        # Check for direction
        category = self.direction(command)
        if category:
            if category[1] == 0:
                return ('direction', category[0])
            return ('go to location', category[0])
        
        # Check for description

        # Check for examination

        # Check for take

        # Check for drop


    
    def direction(self, command):
        # Return type:
        # (direction, 0) if valid direction
        # (location, 1) if already discovered location
        command = command.lower()
        if command == 'n' or command == 'north' or command == 'go north':
            return ('north', 0)
        elif command == 's' or command == 'south' or command == 'go south':
            return ('south', 0)
        elif command == 'e' or command == 'east' or command == 'go east':
            return ('east', 0)
        elif command == 'w' or command == 'west' or command == 'go west':
            return ('west', 0)
        elif command == 'in' or command == 'go in':
            return ('in', 0)
        elif command == 'out' or command == 'go out':
            return ('out', 0)
        else:
            tokens = tokenize(command)
            if len(tokens) > 2:
                if tokens[0] == 'go' and tokens[1] == 'to':
                    loc = ''
                    for i in range(2, len(tokens)):
                        loc += tokens[i]
                        loc += ' '
                    loc = loc[:-1]
                    loc = loc.lower()
                    # go through all the locations
                    for l in self.drama_manager.game_state.locations.keys():
                        if l == loc:
                            if self.drama_manager.game_state.locations[l].isDiscovered:
                                return (l, 1)
                            break
            return None
