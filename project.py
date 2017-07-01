from tile import * 
from board import * 
import graph
import vertex

def read_tiles_file(file_name):
	with open(file_name) as f:
		lines = f.readlines()
		tiles = []
		for x in lines:
			x = x.strip()
			if (len(x) > 0 and x[0] != "#"):
				tile_info = x.split(",")
				tiles.append(Tile(int(x[0]), x[1].lower(), x[2], x[3]))
	return tiles

def main():
    board = Board(read_tiles_file("tiles.txt"))
    # add docks

if __name__ == "__main__": main()