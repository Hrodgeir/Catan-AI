""" Tile Class """
class Tile():
	""" Tiles represent the type and number associated to each hex
	"""

	def __init__(self, Id, tile_type, robber, dice_value):
		self.Id = Id
		self.tile_type = tile_type
		self.robber = robber
		self.dice_value = dice_value

	def get_tile_type(self):
		""" Gets the type of the placement """
		return self.tile_type

	def get_dice_value(self):
		""" Gets the dice value of the placement """
		return self.get_dice_value
