import random
from functools import reduce

""" Tile Class """
class Tile():
	""" Tiles represent the type and number associated to each hex
	"""

	def __init__(self, Id, tile_type, robber, dice_value):
		self.Id = Id
		self.tile_type = tile_type
		self.robber = robber
		self.dice_value = dice_value
		
	def __repr__(self):
		return repr([self.Id, self.tile_type, self.robber, self.dice_value])

	def get_tile_type(self):
		""" Gets the type of the placement """
		return self.tile_type

	def get_dice_value(self):
		""" Gets the dice value of the placement """
		return self.dice_value

	@staticmethod
	def generate_layout():
		""" Generates a random 19 tile board layout """
		tile_catalogue = { 'stone': 3, 'sheep': 4, 'wood': 4, 'brick': 3, 'wheat': 4, 'desert': 1 }
		tile_groups = [[type] * num for type, num in tile_catalogue.items()]
		tiles = sum(tile_groups, [])
		white_tokens = [2, 3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 12]
		red_tokens = [6, 6, 8, 8]
		
		random.shuffle(tiles)
		random.shuffle(white_tokens)
		random.shuffle(red_tokens)
		
		# Choose red token spaces. Ensure that no two red tokens are adjacent.
		adjacency = Tile.compute_adjacency(5, 5)
		red_spaces = []
		red_candidates = [x for x in range(19) if tiles[x] != "desert"]
		for i in red_tokens:
			choice = random.choice(red_candidates)
			red_spaces.append(choice)
			red_candidates = [x for x in red_candidates if x != choice and x not in adjacency[choice]]
		
		# Generate tiles
		layout = []
		for i in range(19):
			id = i + 1
			type = tiles.pop(0)
			robber = False
			token = 0
			
			if type == "desert":
				robber = True
			elif i in red_spaces:
				token = red_tokens.pop()
			else:
				token = white_tokens.pop()
			
			layout.append(Tile(id, type, robber, token))
		
		return layout
	
	@staticmethod
	def compute_adjacency(width, height):
		""" Computes the tile adjacency for a tile layout of the given width and height """
		adjacency = []
		
		mid = int(height / 2)
		for i in range(height):
			tier_start = len(adjacency)
			tier_width = width - abs(i - mid)
			k1 = (0 if i <= mid else 1)
			k2 = (0 if i < mid else 1)
			
			for j in range(tier_width):
				index = tier_start + j
				hasTop = (i > 0)
				hasBottom = (i < height - 1)
				hasLeft = (j > 0)
				hasRight = (j < tier_width - 1)

				adjacent = []
				if hasLeft: adjacent.append(index - 1)
				if hasRight: adjacent.append(index + 1)
				if hasTop and (hasLeft or i > mid): adjacent.append(index - tier_width - k1)
				if hasTop and (hasRight or i > mid): adjacent.append(index - tier_width - k1 + 1)
				if hasBottom and (hasLeft or i < mid): adjacent.append(index + tier_width - k2)
				if hasBottom and (hasRight or i < mid): adjacent.append(index + tier_width - k2 + 1)
				
				adjacency.append(adjacent)
		
		return adjacency
