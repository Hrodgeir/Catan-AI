import tkinter as tk
from board import *

class Display(tk.Frame):
    def __init__(self, board):
        self.master = tk.Tk()
        super().__init__(self.master)

        self.pack()
        self.initialize_window()

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
            canvas = tk.Canvas(self.master, width=400, height=300)
            canvas.pack()

            # Create a line for each edge in the vertex graph
            for vertex in board.vertex_graph.adjacencyList():
                print(vertex)

            coords = {1: {2, 1}, 2: {3, 0}}
            
            # 1
            canvas.create_line(155, 30, 180, 5) # 1 - 2
            canvas.create_line(155, 30, 155, 55) # 1 - 9

            # 2
            canvas.create_line(180, 5, 205, 30) # 2 - 3

            # 3
            canvas.create_line(205, 30, 205, 55) # 3 - 11
            canvas.create_line(205, 30, 230, 5) # 3 - 4

        else:
            return False
