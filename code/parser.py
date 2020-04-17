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

def untokenize(words):
    # Put words together and separate them by space character
    text = ''
    for word in words:
        text += word
        text += ' '
    return text[:-1]

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
                return ['direction', category[0]]
            return ['go to location', category[0]]
        
        category = command
        tokens = tokenize(category) # command splitted
        # Check for description
        if category.lower() == 'look around':
            return ['look around']
        # Check for inventory
        if category.lower() == 'inventory' or category == 'i':
            return ['inventory']
        # Check for examination
        if len(tokens) > 1 and tokens[0] == 'examine':
            return ['examine', untokenize(tokens[1:])]
        # Check for take
        if len(tokens) > 1 and tokens[0] == 'take':
            return ['take', untokenize(tokens[1:])]
        # Check for drop
        if len(tokens) > 1 and tokens[0] == 'drop':
            return ['drop', untokenize(tokens[1:])]
        else:
            # check for special command
            return ['special', command]
    
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
            return None