import tkinter as tk
from tkinter import font
from board import *

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Display(tk.Frame):
    def __init__(self, board_states, players, winner):
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

        # Draw the generated board, aka first board state
        self.initialize_board(board_states, players, winner)

    def initialize_window(self):
        """
        Initializes the graphical user interface window.
        """

        self.master.title("Catan AI Display")

        # Set size of window and central start location
        w = 780
        h = 680
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw/2) - (w/2)
        y = (sh/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    def initialize_board(self, board_states, players, winner):
        """
        Initializes the graphical elements of the board.
        """

        # Initialize canvas
        canvas = tk.Canvas(self.master, width=800, height=680)
        canvas.config(highlightthickness=0, borderwidth=0)
        canvas.place(x=0, y=0)

        # Initialize the edges
        self.initialize_edges(canvas, board_states[0])

        # Initialize the vertices
        self.initialize_vertices(canvas, board_states[0])

        # Initialize the tile info
        self.initialize_tile_info(canvas, board_states[0])

        # Initialize the player info
        self.initialize_player_info(canvas, board_states[0], players)

        # Keep track of the current state
        self.state = 0
        self.lbl_state = tk.Label(canvas, text=("Round: {}".format(self.state)), font=self.header)
        self.lbl_state.place(x=10, y=10)

        # Keep track of the dice value rolled
        self.lbl_dice_value = tk.Label(canvas, text=("Dice Value: {}".format(board_states[0].current_roll)), font=self.header)
        self.lbl_dice_value.place(x=10, y=30)

        # Keep track of the decision made
        self.lbl_decision = tk.Label(canvas, text=("Decision Made: "), font=self.header)
        self.lbl_decision.place(x=10, y=625)

        # Create a button to go to the first board state
        self.btn_next_state = tk.Button(canvas, text="First Round", font=self.header,
                                        command=lambda : self.update(canvas, board_states, 0))
        self.btn_next_state.place(x=75, y=500)

        # Create a button to go to the previous board state
        self.btn_previous_state = tk.Button(canvas, text="Previous Round", font=self.header,
                                            command=lambda : self.update(canvas, board_states, self.state-1))
        self.btn_previous_state.place(x=225, y=500)

        # Create a button to go to the next board state
        self.btn_next_state = tk.Button(canvas, text="Next Round", font=self.header,
                                        command=lambda : self.update(canvas, board_states, self.state+1))
        self.btn_next_state.place(x=420, y=500)

        # Create a button to go to the last board state
        self.btn_next_state = tk.Button(canvas, text="Last Round", font=self.header,
                                        command=lambda : self.update(canvas, board_states, len(board_states)-1))
        self.btn_next_state.place(x=575, y=500)

    def initialize_vertices(self, canvas, board):
        """
        Creates points representing each possible placement.
        """

        self.lst_ovals = []

        # Keep track of the coordinate index
        i = 0
        for c in self.coords:
            x = c.x * 40 + 200
            y = c.y * 40 + 25
            
            # Create a new oval object and add it to the list
            self.lst_ovals.append(canvas.create_oval(x-6, y-6, x+6, y+6, fill='white', width=2))
            i += 1
    
    def update(self, canvas, board_states, new_state):
        """
        Updates the board when the next round button is clicked.
        """

        # Return if out of bounds
        if new_state < 0 or new_state > len(board_states) - 1:
            return

        # Get the board state
        board = board_states[new_state]

        # Keep track of the oval index
        i = 0
        for oval in self.lst_ovals:
            vtx = board.vertices[i]
            if vtx.owner != None:
                colour = '#60B7FF'
                if vtx.is_city:
                    colour = '#005399'
            else:
                colour = 'white'
            
            canvas.itemconfig(oval, fill=colour)
            i += 1
        
        # Update the board state
        self.state = new_state
        self.lbl_state.config(text=("Round: {}".format(self.state)))

        # Update dice roll
        self.lbl_dice_value.config(text=("Dice Value: {}".format(board_states[self.state].current_roll)))

        # Update the decision made
        decision_made = board.player_state[0].decision.replace("_"," ").title()
        self.lbl_decision.config(text=("Decision Made: {}".format(decision_made)))

        # Update the resource card count
        player = board_states[new_state].player_state[0]
        for key, value in player.resources.items():
            if key == 'wheat':
                card = self.card_wheat
            elif key == 'brick':
                card = self.card_brick
            elif key == 'wood':
                card = self.card_wood
            elif key == 'stone':
                card = self.card_stone
            elif key == 'sheep':
                card = self.card_sheep
            canvas.itemconfig(card, text=('{}'.format(player.resources[key])))
        
        # Update the knight count
        canvas.itemconfig(self.card_knights, text=('{}'.format(player.knights)))

        # Update the score value
        canvas.itemconfig(self.player_score, text=('{}'.format(player.points)))

    def initialize_edges(self, canvas, board):
        """
        Creates the edges between the vertices.
        """

        i = 0
        for v in board.vertices:
            coord = self.coords[i]

            x = coord.x * 40 + 200
            y = coord.y * 40 + 25

            for n in v.neighbours:
                nCoord = self.coords[n-1]
                nx = nCoord.x * 40 + 200
                ny = nCoord.y * 40 + 25
                canvas.create_line(x, y, nx, ny, width=2)

            i = i + 1
    
    def initialize_tile_info(self, canvas, board):
        """
        Display the tile info in the middle of each tile.
        """

        i = 0
        for t in board.tiles:
            tile_type = t.get_tile_type()
            dice_value = int(t.get_dice_value())
            coord = self.tile_coords[i]

            x = coord.x * 40 + 240
            y = coord.y * 80 + 78

            canvas.create_text(x, y, text=tile_type.title(), font=self.header)

            # Brighter red corresponds to a higher probability 
            # that the specific tile dice value is rolled
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

    def initialize_player_info(self, canvas, board, players):
        """
        Initialize the player info and score below the board.
        """

        # Display the column names
        canvas.create_text(50, 570, text="Player", font=self.header)
        canvas.create_text(175, 570, text="Strategy", font=self.header)
        canvas.create_text(300, 570, text="Wheat", font=self.header)
        canvas.create_text(375, 570, text="Brick", font=self.header)
        canvas.create_text(450, 570, text="Wood", font=self.header)
        canvas.create_text(525, 570, text="Stone", font=self.header)
        canvas.create_text(600, 570, text="Sheep", font=self.header)
        canvas.create_text(675, 570, text="Knights", font=self.header)
        canvas.create_text(750, 570, text="Score", font=self.header)

        # Display the player information
        canvas.create_rectangle(10, 590, 20, 600, fill='#60B7FF')
        canvas.create_text(60, 595, text="Player 1", font=self.default)
        canvas.create_text(175, 595, text=players[0].strategy, font=self.default)

        # Initialize the card counts
        self.card_wheat = canvas.create_text(300, 595, text="0", font=self.default)
        self.card_brick = canvas.create_text(375, 595, text="0", font=self.default)
        self.card_wood = canvas.create_text(450, 595, text="0", font=self.default)
        self.card_stone = canvas.create_text(525, 595, text="0", font=self.default)
        self.card_sheep = canvas.create_text(600, 595, text="0", font=self.default)
        self.card_knights = canvas.create_text(675, 595, text="0", font=self.default)

        # Initialize the player score
        self.player_score = canvas.create_text(750, 595, text="0", font=self.default)
