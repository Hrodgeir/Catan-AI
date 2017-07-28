import tkinter as tk
from board import *

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Display(tk.Frame):
    def __init__(self, board):
        # Initialize the GUI
        self.master = tk.Tk()
        super().__init__(self.master)
        self.pack()
        self.initialize_window()

        # Set the coordinates
        self.coords = [
            Coordinate(2,1), #1
            Coordinate(3,0), #2
            Coordinate(4,1), #3
            Coordinate(5,0), #4
            Coordinate(6,1), #5
            Coordinate(7,0), #6
            Coordinate(8,1), #7

            Coordinate(1,3), #8
            Coordinate(2,2), #9
            Coordinate(3,3), #10
            Coordinate(4,2), #11
            Coordinate(5,3), #12
            Coordinate(6,2), #13
            Coordinate(7,3), #14
            Coordinate(8,2), #15
            Coordinate(9,3), #16

            Coordinate(0,5), #17
            Coordinate(1,4), #18
            Coordinate(2,5), #19
            Coordinate(3,4), #20
            Coordinate(4,5), #21
            Coordinate(5,4), #22
            Coordinate(6,5), #23
            Coordinate(7,4), #24
            Coordinate(8,5), #25
            Coordinate(9,4), #26
            Coordinate(10,5), #27

            Coordinate(0,6), #28
            Coordinate(1,7), #29
            Coordinate(2,6), #30
            Coordinate(3,7), #31
            Coordinate(4,6), #32
            Coordinate(5,7), #33
            Coordinate(6,6), #34
            Coordinate(7,7), #35
            Coordinate(8,6), #36
            Coordinate(9,7), #37
            Coordinate(10,6), #38

            Coordinate(1,8), #39
            Coordinate(2,9), #40
            Coordinate(3,8), #41
            Coordinate(4,9), #42
            Coordinate(5,8), #43
            Coordinate(6,9), #44
            Coordinate(7,8), #45
            Coordinate(8,9), #46
            Coordinate(9,8), #47

            Coordinate(2,10), #48
            Coordinate(3,11), #49
            Coordinate(4,10), #50
            Coordinate(5,11), #51
            Coordinate(6,10), #52
            Coordinate(7,11), #53
            Coordinate(8,10)  #54
        ]

        # Set the tile coordinates
        self.tile_coords = [
            Coordinate(2,0), #1
            Coordinate(4,0), #2
            Coordinate(6,0), #3

            Coordinate(1,1), #4
            Coordinate(3,1), #5
            Coordinate(5,1), #6
            Coordinate(7,1), #7

            Coordinate(0,2), #8
            Coordinate(2,2), #9
            Coordinate(4,2), #10
            Coordinate(6,2), #11
            Coordinate(8,2), #12

            Coordinate(1,3), #13
            Coordinate(3,3), #14
            Coordinate(5,3), #15
            Coordinate(7,3), #16

            Coordinate(2,4), #17
            Coordinate(4,4), #18
            Coordinate(6,4)  #19
        ]

        # Draw the generated board
        self.draw_board(board)

    def initialize_window(self):
        """
        Initializes the graphical user interface window.
        """

        self.master.title("Catan AI Display")

        # Set size of window and central start location
        w = 640
        h = 720
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw/2) - (w/2)
        y = (sh/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def draw_board(self, board):
        """
        Draw the generated board.
        """

        # Initialize canvas
        canvas = tk.Canvas(self.master, width=720, height=720)
        canvas.config(highlightthickness=0, borderwidth=0)
        canvas.place(x=0, y=100)

        # Draw the edges
        self.display_edges(canvas, board)
        
        # Draw the vertices
        self.display_vertices(canvas, board)

        # Display the tile info
        self.display_tile_info(canvas, board)

    def display_vertices(self, canvas, board):
        """
        Creates points representing each placement.
        """

        for c in self.coords:
            x = c.x * 40 + 125
            y = c.y * 40 + 5
            canvas.create_oval(x-5, y-5, x+5, y+5, fill="#FFFFFF")

    def display_edges(self, canvas, board):
        """
        Creates the edges between the placements.
        """

        i = 0
        for v in board.vertices:
            coord = self.coords[i]

            x = coord.x * 40 + 125
            y = coord.y * 40 + 5

            for n in v.neighbours:
                nCoord = self.coords[n-1]
                nx = nCoord.x * 40 + 125
                ny = nCoord.y * 40 + 5
                canvas.create_line(x, y, nx, ny)

            i = i + 1
    
    def display_tile_info(self, canvas, board):
        """
        Display the tile info in the middle of each tile.
        """

        i = 0
        for t in board.tiles:
            tile_type = t.get_tile_type()
            dice_value = t.get_dice_value()
            coord = self.tile_coords[i]

            x = coord.x * 40 + 165
            y = coord.y * 80 + 60

            canvas.create_text(x, y, text=tile_type)
            canvas.create_text(x, y+20, text=dice_value)
            
            i += 1
