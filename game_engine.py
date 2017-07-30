import random
from vertex import *

class GameEngine:
    def roll_dice(self):
        """
        Represent the roll of two dice as two random picks between 1 and 6\n
        :return: The sum of two random numbers between 1 and 6
        """
        return random.randint(1, 6) + random.randint(1, 6)

    #TODO: actually test this method
    def give_resources_by_dice_roll(self, board, players, dice_val):
        rewarded_tiles = board.tile_by_dice_val[str(dice_val)]

        for vertex in board.vertices:
            for tile in rewarded_tiles:
                if vertex.tile_id == tile:
                    resource = players[str(vertex.owner)].resources[tile_type] #hope it actually caches the reference
                    resource = resource + 1

    def setup_rounds(self, players, current_board, total_rounds=2):
        """
        Begin setup phase of Catan\n
        :param players: The list of players playing the game\n
        :param current_board: The current state of the board as a board object\n
        :param total_rounds: OPTIONAL, the number of rounds to play, default 2
        """
        round_counter = 0

        while(round_counter < total_rounds):
            for player in players:
                #print("Player " + str(player.id))
                #do stuff
                current_board = self.place_settlement(current_board, player)

            for player in reversed(players):
                #do stuff again
                print("Player " + str(player.id))
            
            round_counter = round_counter + 2

    def place_settlement(self, current_board, player):
        """
        Place a settlement on the current playing board\n
        :param current_board: The current state of the board as a board object\n
        :param player: The player object who will be placing a settlement\n
        :return: The new state of the board
        """

        #avail_vertices = current_board.get_available_vertices()

        #find best placement
        vertex_id = self.search_board(current_board, player.strategy)

        current_board.vertices[vertex_id].set_owner(player)

        return current_board

    def search_board(self, current_board, strategy):
        """
        Find the best place to place a settlment based on the current layout of the board\n
        :param current_board: The current state of the board as a board object\n
        :param strategy: The strategy of the player who will be placing a settlement\n
        :return: The vertex id to place on
        """
        vertex_id = 0



        return vertex_id 
            
            
        
            



        
    
        
