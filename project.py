import argparse

import vertex
from board import *
from display import *
from player import *
from game_engine import *


def play_game(random):
    try:    
        board = Board(random)
        engine = GameEngine()
        players = {}
        i = 1

        # create players
        while (i <= 4):
            players.append(Player(i, None))
            i = i + 1
    
        # the vertices that we have to iterate over and make calculations to choose the best
        avail_vertices = board.get_available_vertices()

        engine.positioning_turns(players)

        # Initialize the display
        display = Display(board)

        # Run the display
        display.mainloop()

    except ValueError:
        print("Check .txt files")

    except AssertionError:
        print("Check .txt files")

def main():

    parser = argparse.ArgumentParser(description="Play the AI")
    
    # Run with random board
    parser.add_argument('-r', action='store_true')
    
    # Run with file input board
    parser.add_argument('-f', action='store_true')

    # Parse the input args
    args = parser.parse_args()

    if args.r:
        play_game(True)

    elif args.f:
        play_game(False)
            
    else:
        parser.print_help()

if __name__ == "__main__": 
    """
    project.py
    """
    
    main()
