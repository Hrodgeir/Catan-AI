""" Tile Class """
class Tile():
    """ Tiles represent the type and number associated to each hex
    """

    def __init__(self, tile_type, dice_value):
        self.tile_type = tile_type
        self.dice_value = dice_value

    def get_tile_type(self):
        """ Gets the type of the placement """
        return self.tile_type

    def get_dice_value(self):
        """ Gets the dice value of the placement """
        return self.get_dice_value
