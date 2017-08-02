import argparse

import vertex
from board import *
from display import *
from player import *
from game_engine import *

def play_game(random, num_players=4):
    """
    Run the game\n
    :param random: Boolean, if true, a random board is created otherwise it is a preset board from .txt's\n
    :param num_players: OPTIONAL, the number of players who will be playing the game
    """
    try:    

        if num_players > 4 or num_players < 1:
            raise ValueError

        board = Board(random)
        engine = GameEngine()
        players = []
        i = 1

        if random:
            strategy_list = Player.generate_strategies(num_players)
        else:
            strategy_list = Player.read_strategies(num_players, "strategies.txt")

        # create players
        while (i <= num_players):
            players.append(Player(i, strategy_list[i-1]))
            i = i + 1
    
        # the vertices that we have to iterate over and make calculations to choose the best

        board = engine.setup_rounds(players, board)
        print(board.__repr__)

        # Initialize the display
        display = Display(board, players)

        # Run the display
        display.mainloop()

    except ValueError:
        print("The number of playes must be 4 or less")

    except AssertionError:
        print("Check .txt files")

def main():
    """
    Play the game with either a random board or a preset board
    """
    parser = argparse.ArgumentParser(description="Play the AI")
    
    # Run with random board
    parser.add_argument('-r', action='store_true', help='Run with random values')
    
    # Run with file input board
    parser.add_argument('-f', action='store_true', help='Run with values read from files')

    parser.add_argument("-p", type=int, default=4, help='The number of players')             

    # Parse the input args
    args = parser.parse_args()

    if args.r:
        play_game(True, args.p)

    elif args.f:
        play_game(False, args.p)
            
    else:
        parser.print_help()

if __name__ == "__main__": 
    """
    project.py
    """
    
    main()
