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

        """self.directions = ['north', 'south', 'west', 'east']
        self.actions = ['go', 'take', 'drop'] """
    
"""     def processCommand(self, command):
        tokens = tokenize(command)
        if len(tokens) == 0:
            return 'That is not valid.'
        if tokens[0] in  self.actions:
            if tokens[0] == 'go':
                if len(tokens) == 1:
                    return 'Where?'
                else:
                    if tokens[1] in self.directions:
                        return 'Going ' + tokens[1]
        else:
            return 'That is not valid.' """
        