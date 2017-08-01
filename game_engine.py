import random
from vertex import *

class GameEngine:
    """
    Game Engine controller
    """
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
                    #resource = players[str(vertex.owner)].resources[tile_type] #hope it actually caches the reference
                    #resource = resource + 1
                    pass

    def setup_rounds(self, players, current_board, total_rounds=2):
        """
        Begin setup phase of Catan\n
        :param players: The list of players playing the game\n
        :param current_board: The current state of the board as a board object\n
        :param total_rounds: OPTIONAL, the number of rounds to play, default 2
        :return: The state of the board after setup rounds
        """
        round_counter = 0

        while(round_counter < total_rounds):
            for player in players:
                #print("Player " + str(player.id))
                current_board = self.place_settlement(current_board, player)

            for player in reversed(players):
                #print("Player " + str(player.id))
                current_board = self.place_settlement(current_board, player)
            
            # two rounds have passed
            round_counter = round_counter + 2

        return current_board

    def place_settlement(self, current_board, player):
        """
        Place a settlement on the current playing board\n
        :param current_board: The current state of the board as a board object\n
        :param player: The player object who will be placing a settlement\n
        :return: The new state of the board
        """

        #find best placement
        vertex_id = self.search_board(current_board, player.strategy)
        current_board.vertices[vertex_id-1].set_owner(player)
        return current_board

    def search_board(self, current_board, strategy):
        """
        Find the best place to place a settlment based on the current layout of the board\n
        :param current_board: The current state of the board as a board object\n
        :param strategy: The strategy of the player who will be placing a settlement\n
        :return: The vertex id to place on
        """
        scores = {}

        # set score of each vertex to 0
        for vertex in current_board.get_available_vertices():
            scores[vertex] = 0

        # get the tiles related to each available vertex
        for vertex in current_board.get_available_vertices():
            tiles = vertex.tile_id
            for tile in tiles:
                tile_type = current_board.tiles[tile-1].get_tile_type()
                scores[vertex] += GameEngine.get_score(tile_type, strategy)

        best_score = 0
        vertex_id = next(iter(scores))

        #find the best vertex for placement
        for key, value in scores.items():
            if value > best_score:
                best_score = value
                vertex_id = key

        return vertex_id.name 

    @staticmethod
    def get_score(tile_type, strategy):
        """
        :param tile_type: The type of the tile
        :param strategy: The strategy the player is using
        :return: The score the tile adds to the vertex
        """
        # weight_array: [stone, sheep, wood, brick, wheat]

        if strategy is "cities":
            weight_array = [1,0.5,0.5,0.5,1]
        elif strategy is "settlements":
            weight_array = [0.5,1,1,1,1]
        #TODO: figure out the best way to deal with different tile type monopolies
        elif strategy is "monopoly": #currently sheep
            weight_array = [0.5,1,0.5,0.5,0.5]
        elif strategy is "development":        
            weight_array = [1,1,0.5,0.5,1]
        else:
            weight_array = [1,1,1,1,1]
        
        return GameEngine.determine_score(tile_type, weight_array)

    @staticmethod
    def determine_score(tile_type, weight_array):
        """
        :param tile_type: The tile type
        :param weight_array: An array of weights that correspond to each tile type and its related strategy
        :return: 1 * the weight
        """
        if tile_type is "stone":
            return 1*weight_array[0]
        elif tile_type is "sheep":
            return 1*weight_array[1]
        elif tile_type is "wood":
            return 1*weight_array[2]
        elif tile_type is "brick":
            return 1*weight_array[3]
        elif tile_type is "wheat":
            return 1*weight_array[4]
        else:
            return 0

        
    
        
