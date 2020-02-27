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
        return 'this'
        