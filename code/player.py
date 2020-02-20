# Player
from character import Character

class Player(Character):

    def __init__(self, name="", location=None):
        super.__init__(name, location)

    # Set the name of the player
    def set_name(self, new_name):
        self.name = new_name
