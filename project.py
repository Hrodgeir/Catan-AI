from board import *
from display import *
from player import *
from game_engine import *
import vertex

def main():
    try:
        board = Board()
        engine = GameEngine()
        players = []
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

if __name__ == "__main__": main()
