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
            Coordinate(8,10), #54
        ]

        # Draw the generated board
        self.draw_board(board)

    def initialize_window(self):
        self.master.title("Catan AI Display")

        # Set size of window and central start location
        w = 800
        h = 600
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw/2) - (w/2)
        y = (sh/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def draw_board(self, board):
        if isinstance(board, Board):
            # Initialize canvas
            canvas = tk.Canvas(self.master, width=500, height=500)
            canvas.place(x=150, y=50)

            # Draw the edges
            i = 0
            for v in board.vertices:
                self.create_edges(canvas, self.coords[i], v)
                i = i + 1
            
            # Draw the vertices
            for c in self.coords:
                self.create_point(canvas, c)

        else:
            return False

    def create_point(self, canvas, coord):
        if isinstance(coord, Coordinate):
            x = coord.x * 25 + 125
            y = coord.y * 25 + 5
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#FFFFFF")
        else:
            return False

    def create_edges(self, canvas, coord, vertex):
        if isinstance(vertex, Vertex):
            x = coord.x * 25 + 125
            y = coord.y * 25 + 5
            for n in vertex.neighbours:
                nCoord = self.coords[n-1]
                nx = nCoord.x * 25 + 125
                ny = nCoord.y * 25 + 5
                canvas.create_line(x, y, nx, ny)
        else:
            return False
