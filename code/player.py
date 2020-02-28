# Player
from character import Character

class Player(Character):

    def __init__(self, name="", location=None):
        super(Player, self).__init__(name, location, True)

    # Set the name of the player
    def set_name(self, new_name):
        self.name = new_name
