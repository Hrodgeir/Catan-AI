import random
from vertex import *

class GameEngine:
    """
    Game Engine controller
    """

    @staticmethod
    def roll_dice():
        """
        Represent the roll of two dice as two random picks between 1 and 6\n
        :return: The sum of two random numbers between 1 and 6
        """
        return random.randint(1, 6) + random.randint(1, 6)

    #TODO: actually test this method
    def give_resources_by_dice_roll(self, board, players, dice_val):
        rewarded_tiles = board.tile_by_dice_val[str(dice_val)]

        for vertex in board.vertices:
            if vertex.owner != None:
                for tile_id in rewarded_tiles:
                    if tile_id in vertex.tile_id:
                        tile = board.tiles[tile_id - 1]
                        type = tile.tile_type
                        
                        resources = players[vertex.owner.id - 1].resources
                        resources[type] = resources[type] + 1

    def setup_rounds(self, players, current_board, total_rounds=2):
        """
        Begin setup phase of Catan\n
        :param players: The list of players playing the game\n
        :param current_board: The current state of the board as a board object\n
        :param total_rounds: OPTIONAL, the number of rounds to play, default 2
        :return: The state of the board after setup rounds
        """
        round_counter = 0
        reverse = False

        while(round_counter < total_rounds):
            order = (players if not reverse else reversed(players))
            for player in order:
                #print("Player " + str(player.id))
                current_board = self.place_settlement(current_board, player)
            
            round_counter = round_counter + 1
            reverse = not reverse

        return current_board

    def take_turn(self, players, current_board):
        """
        """
        for player in players:
            current_board.current_roll = GameEngine.roll_dice()
            self.give_resources_by_dice_roll(current_board, players, current_board.current_roll)
            decision, vertex = self.evaluate_decision(player, current_board)
            current_board = self.do_decision(player, decision, current_board, vertex)

        return current_board

    def evaluate_decision(self, player, current_board):
        """
        """
        decisions = ["do_nothing", "build_settlement", "build_city", "build_road", "draw_development", "trade"]
        decision = "do_nothing"
        vertex = None
        highest_score = 0.5
        
        build_city_scores = self.calculate_city_scores(player, current_board)
        build_settlement_scores = self.calculate_settlement_scores(player, current_board)
        build_development_score = self.calculate_development_score(player, current_board)
        trade_score = self.calculate_trade_score(player, current_board)
        
        for idx, score in enumerate(build_city_scores):
            if score > highest_score:
                highest_score = score
                vertex = current_board.vertices[idx]
                decision = "build_city"
        
        for idx, score in enumerate(build_settlement_scores):
            if score > highest_score:
                highest_score = score
                vertex = current_board.vertices[idx]
                decision = "build_settlement"
        
        if build_development_score > highest_score:
            highest_score = build_development_score
            vertex = None
            decision = "draw_development"
        
        if trade_score > highest_score:
            highest_score = trade_score
            vertex = None
            decision = "trade"
        
        return decision, vertex

    def score_buyable(self, player, item):
        if item == "build_settlement":
            return self.score_settlement(player)
        elif item == "build_city":
            return self.score_city(player)
        elif item == "build_road":
            return self.score_road(player)
        elif item == "draw_development":
            return self.score_development_card(player)
        else:
            print("Something went wrong when trying to score buyable")
            return 0

    def do_decision(self, player, decision, current_board, vertex):
        """
        """

        if decision == "trade":
            pass
        elif decision == "build_settlement":
            idx = vertex.name - 1
            distance = player.vertex_distances[idx]
            player.resources["wood"] = player.resources["wood"] - distance - 1
            player.resources["brick"] = player.resources["brick"] - distance - 1
            player.resources["wheat"] = player.resources["wheat"] - 1
            player.resources["sheep"] = player.resources["sheep"] - 1
            vertex.set_owner(player)
        elif decision == "build_city":
            pass
        elif decision == "build_road":
            pass
        elif decision == "draw_development":
            current_board = self.draw_development_card(current_board)
            return current_board

        else: #"do_nothing"
           
            return current_board
    
    def calculate_city_scores(self, player, current_board):
        return [0 for vtx in current_board.vertices]
    
    def calculate_settlement_scores(self, player, current_board):
        resources = player.resources
        amounts = [resources["wood"], resources["brick"], resources["wheat"], resources["sheep"]]
        
        scores = [0 for vtx in current_board.vertices]
        if any(x == 0 for x in amounts):
            return scores
        
        for vtx in current_board.vertices:
            idx = vtx.name - 1
            distance = player.vertex_distances[idx]
            costs = [distance + 1, distance + 1, 1, 1]
            after = [amounts[i] - costs[i] for i in range(len(amounts))]
            
            if vtx.owner is not None:
                continue
            if any([current_board.vertices[id - 1].owner is not None for id in vtx.neighbours]):
                continue
            if any([x < 0 for x in after]):
                continue
            
            scores[idx] = (2 - distance) * 0.1
            for tile_id in vtx.tile_id:
                tile_idx = tile_id - 1
                tile = current_board.tiles[tile_idx]
                tile_type = tile.get_tile_type()
                base_score = GameEngine.get_score(tile_type, player.strategy)
                scores[idx] += base_score # tile.probability
            
        return scores
    
    def calculate_development_score(self, player, current_board):
        return 0
    
    def calculate_trade_score(self, player, current_board):
        return 0

    def draw_development_card(current_board):
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
        vertex = current_board.vertices[vertex_id-1]
        
        vertex.set_owner(player)
        player.update_distances(vertex, current_board)
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

        if strategy == "cities":
            weight_array = [1,0.5,0.5,0.5,1]
        elif strategy == "settlements":
            weight_array = [0.5,1,1,1,1]
        #TODO: figure out the best way to deal with different tile type monopolies
        elif strategy == "stone_monopoly": #currently sheep
            weight_array = [1,0.5,0.5,0.5,0.5]
        elif strategy == "sheep_monopoly": #currently sheep
            weight_array = [0.5,1,0.5,0.5,0.5]
        elif strategy == "wood_monopoly": #currently sheep
            weight_array = [0.5,0.5,1,0.5,0.5]
        elif strategy == "brick_monopoly": #currently sheep
            weight_array = [0.5,0.5,0.5,1,0.5]
        elif strategy == "wheat_monopoly": #currently sheep
            weight_array = [0.5,0.5,0.5,0.5,1]
        elif strategy == "development":        
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
        if tile_type == "stone":
            return 1*weight_array[0]
        elif tile_type == "sheep":
            return 1*weight_array[1]
        elif tile_type == "wood":
            return 1*weight_array[2]
        elif tile_type == "brick":
            return 1*weight_array[3]
        elif tile_type == "wheat":
            return 1*weight_array[4]
        else:
            return 0

        
    
        
