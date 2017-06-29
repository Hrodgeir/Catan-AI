""" Board Class """
import placement

class Board():
    """ The board consists of 54 placements
    """

    def __init__(self):
        self.placements = []

        for i in range(54):
            self.placements.append(placement.Placement(None, None, None))

        """ How to generate board? """
