""" Dock Class """
import random

class Dock():
    """ 
    Docks are sometimes associated to coast placements
    """

    def __init__(self, resource):
        self.resource = resource
        if(resource == "all"):
            self.ratio = 3
        else:
            self.ratio = 2

    def get_ratio(self):
        """
        Gets the ratio, ratio:1
        """
        return self.ratio

    def get_resource(self):
        """
        Gets the resource type
        """
        return self.resource

    @staticmethod
    def generate_docks():
        """
        Generate a random order of 9 docks for the board\n
        :return: list of docks
        """
        
        # Establish a list/dictionary of docks to be chosen from
        dock_catalogue = { 'stone': 1, 'sheep': 1, 'wood': 1, 'brick': 1, 'wheat': 1, 'all': 4 }
        dock_groups = [[type] * num for type, num in dock_catalogue.items()]
        docks = sum(dock_groups, [])

        random.shuffle(docks)
        dock_layout = []

        # Create the layout based on the random shuffle
        for i in range(9):
            choice = random.choice(docks)
            dock_layout.append(choice)

        return dock_layout