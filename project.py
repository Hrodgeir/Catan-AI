import argparse
import datetime
import vertex
import copy
from board import *
from display import *
from player import *
from game_engine import *

def play_game(random, num_players=4, testing=False, f=None, strat=None):
    """
    Run the game\n
    :param random: Boolean, if true, a random board is created otherwise it is a preset board from .txt's\n
    :param num_players: OPTIONAL, the number of players who will be playing the game
    """
    try:    
        if num_players > 4 or num_players < 1:
            raise ValueError

        board_states = []
        engine = GameEngine()
        players = []
        i = 1
        winner = None

        if random:
            strategy_list = Player.generate_strategies(num_players)
        else:
            strategy_list = Player.read_strategies(num_players, "strategies.txt")

        # create players
        while (i <= num_players):
            if strat is not None:
                 players.append(Player(i, strat))
            else:
                players.append(Player(i, strategy_list[i-1]))
            i = i + 1
        
        current_board = Board(random)
        current_board.player_state = players
        board_states.append(copy.deepcopy(current_board))

        # the vertices that we have to iterate over and make calculations to choose the best

        engine.setup_rounds(players, current_board)
        board_states.append(copy.deepcopy(current_board))
        
        rounds = 300
        has_won = False

        for i in range(rounds):
            engine.take_turn(players, current_board)
            board_states.append(copy.deepcopy(current_board))
            winner = engine.evaluate_win(players)
            if winner != None:
                break

        if not testing:
            # Initialize the display
            display = Display(board_states, players, winner)

            # Run the display
            display.mainloop()
        else:
            player = players[0]
            if f is not None:
                f.write(player.strategy + ",")
                f.write(str(len(board_states)) + ",")
                f.write(str(player.points) + ",")
                if winner is not None:
                    f.write("1\n")
                else:
                    f.write("0\n")
       
    except ValueError as ex:
        print(ex)
        print("The number of players must be 4 or less")

    except AssertionError as ex:
        print(ex)
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

    # run testing of strategies
    parser.add_argument("-e", action='store_true', help='Start extensive testing')                     

    # Parse the input args
    args = parser.parse_args()

    if args.r:
        if args.e:
            date = datetime.datetime.now().strftime("%H_%M_%S_%dd_%mm_%yyyy")
            f = open("results"+date+".csv", "a")
            f.write("strategy,num_turns,victory_points,win\n")
            for x in range(0, 101):
                for s in ["settlements", "cities", "development", "brick_monopoly", "sheep_monopoly", "wood_monopoly", "stone_monopoly", "wheat_monopoly"]:
                    play_game(True, args.p, True, f, s)
                print("done " + str(x))
            f.close() 
        else:
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
