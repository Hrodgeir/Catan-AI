import tkinter as tk
from tkinter import font
from board import *

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Display(tk.Frame):
    def __init__(self, board, players):
        # Initialize the GUI
        self.master = tk.Tk()
        super().__init__(self.master)
        self.pack()
        self.initialize_window()

        # Setup custom fonts
        self.default = font.Font(family='Verdana', size=12)
        self.header = font.Font(family='Verdana', size=12, weight='bold')

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
        self.draw_board(board, players)

    def initialize_window(self):
        """
        Initializes the graphical user interface window.
        """

        self.master.title("Catan AI Display")

        # Set size of window and central start location
        w = 640
        h = 640
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw/2) - (w/2)
        y = (sh/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def draw_board(self, board, players):
        """
        Draw the generated board.
        """

        # Initialize canvas
        canvas = tk.Canvas(self.master, width=640, height=640)
        canvas.config(highlightthickness=0, borderwidth=0, bg='gray60')
        canvas.place(x=0, y=0)

        # Draw the edges
        self.display_edges(canvas, board)
        
        # Draw the vertices
        self.display_vertices(canvas, board)

        # Display the tile info
        self.display_tile_info(canvas, board)

        # Display the player info
        self.display_player_info(canvas, board, players)

    def display_vertices(self, canvas, board):
        """
        Creates points representing each placement.
        """

        # Keep track of the coordinate index
        i = 0
        for c in self.coords:
            x = c.x * 40 + 125
            y = c.y * 40 + 25
            

            # Check to see if the placement is taken
            placement_owner = board.vertices[i].owner

            if placement_owner != None:
                if placement_owner.id == 1:
                    colour = 'red'
                elif placement_owner.id == 2:
                    colour = 'blue'
                elif placement_owner.id == 3:
                    colour = 'green'
                elif placement_owner.id == 4:
                    colour = 'yellow'
            else:
                colour = 'white'
            
            canvas.create_oval(x-6, y-6, x+6, y+6, fill=colour, width=2)

            i += 1

    def display_edges(self, canvas, board):
        """
        Creates the edges between the placements.
        """

        i = 0
        for v in board.vertices:
            coord = self.coords[i]

            x = coord.x * 40 + 125
            y = coord.y * 40 + 25

            for n in v.neighbours:
                nCoord = self.coords[n-1]
                nx = nCoord.x * 40 + 125
                ny = nCoord.y * 40 + 25
                canvas.create_line(x, y, nx, ny, width=2)

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
            y = coord.y * 80 + 78

            canvas.create_text(x, y, text=tile_type.title(), font=self.header)

            # Brighter red corresponds to a higher probability 
            # that the specific tile dice value is rolled.
            if dice_value == 0:
                dice_colour = '#000000'
            elif dice_value == 2 or dice_value == 12:
                dice_colour = '#2C0007'
            elif dice_value == 3 or dice_value == 11:
                dice_colour = '#59000E'
            elif dice_value == 4 or dice_value == 10:
                dice_colour = '#860015'
            elif dice_value == 5 or dice_value == 9:
                dice_colour = '#B3001C'
            elif dice_value == 6 or dice_value == 8:
                dice_colour = '#E00024'
            
            canvas.create_text(x, y+20, text=dice_value, font=self.header, fill=dice_colour)
            
            i += 1

    def display_player_info(self, canvas, board, players):
        """
        Display the player info and score below the board.
        """

        # Display the column names
        canvas.create_text(150, 530, text="Player", font=self.header)
        canvas.create_text(325, 530, text="Strategy", font=self.header)
        canvas.create_text(500, 530, text="Score", font=self.header)

        # Display the corresponding colour and score for each player.
        for p in players:
            if (p.id == 1):
                canvas.create_rectangle(110, 550, 100, 560, fill='red')
                canvas.create_text(150, 555, text="Player 1", font=self.default)
                canvas.create_text(325, 555, text=p.strategy, font=self.default)
                canvas.create_text(500, 555, text="0", font=self.default)
            elif (p.id == 2):
                canvas.create_rectangle(110, 570, 100, 580, fill='blue')
                canvas.create_text(150, 575, text="Player 2", font=self.default)
                canvas.create_text(325, 575, text=p.strategy, font=self.default)
                canvas.create_text(500, 575, text="0", font=self.default)
            elif (p.id == 3):
                canvas.create_rectangle(110, 590, 100, 600, fill='green')
                canvas.create_text(150, 595, text="Player 3", font=self.default)
                canvas.create_text(325, 595, text=p.strategy, font=self.default)
                canvas.create_text(500, 595, text="0", font=self.default)
            elif (p.id == 4):
                canvas.create_rectangle(110, 610, 100, 620, fill='yellow')
                canvas.create_text(150, 615, text="Player 4", font=self.default)
                canvas.create_text(325, 615, text=p.strategy, font=self.default)
                canvas.create_text(500, 615, text="0", font=self.default)
