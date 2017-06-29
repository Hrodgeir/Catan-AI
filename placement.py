""" Placement Class """
class Placement():
    """ Placements represent where a village can be placed on a board
        They contain a maximum of 3 neighbours and 3 adjacent tiles
    """

    def __init__(self, adj_placements, adj_tiles, dock):
        self.adj_placements = adj_placements
        self.adj_tiles = adj_tiles
        self.dock = dock
        self.owner = None

    def get_owner(self):
        """ Gets the owner of the placement """
        return self.owner

    def set_owner(self, player):
        """ Sets the owner of the placement """
        self.owner = player

    def get_adj_tiles(self):
        """ Gets the adjacent tiles of the placement """
        return self.adj_tiles

    def get_dock(self):
        """ Gets the dock if there is one associated """
        return self.dock
