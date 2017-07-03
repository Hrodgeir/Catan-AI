
from board import *
from player import *
import vertex

def main():
    try:
        board = Board()
        players = {}
        i = 1

        # create players
        while (i <= 4):
            players[i] = Player(i, None)
            i =  i + 1
    
        # the vertices that we have to iterate over and make calculations to choose the best
        avail_vertices = board.get_available_vertices()

    except ValueError:
        print("Check .txt files")

    except AssertionError:
        print("Check .txt files")

    


# add docks

if __name__ == "__main__": main()
