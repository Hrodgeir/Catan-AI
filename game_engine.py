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
                current_board = self.place_settlement(current_board, player)
            
            round_counter = round_counter + 1
            reverse = not reverse

        return current_board

    def take_turn(self, players, current_board):
        """
        Take a turn (Roll Dice, Get Resources, Make a Decision, Do Decision)
        """

        for player in players:
            current_board.current_roll = GameEngine.roll_dice()
            
            self.give_resources_by_dice_roll(current_board, players, current_board.current_roll)
            
            decision, vertex, trade_g, trade_f = self.evaluate_decision(player, current_board)

            # Set the decision for the GUI
            player.decision = decision

            current_board = self.do_decision(player, decision, current_board, vertex, trade_g, trade_f)

        return current_board

    def evaluate_decision(self, player, current_board):
        """
        Evaluate all possible decisions based on weighted heuristics
        """

        decisions = ["do_nothing", "build_settlement", "build_city", "build_road", "draw_development", "trade"]
        decision = "do_nothing"
        vertex = None
        trade_get = None # What to receive from a trade
        trade_from = None # What to trade away
        highest_score = 0.3
        
        build_city_scores = self.calculate_city_scores(player, current_board)
        build_settlement_scores = self.calculate_settlement_scores(player, current_board)
        build_development_score = self.calculate_development_score(player, current_board)
        trade_score, trade_g, trade_f = self.calculate_trade_score(player, current_board)

        print("City: {}".format(max(build_city_scores)))
        print("Sett: {}".format(max(build_settlement_scores)))
        print("Deve: {}".format(build_development_score))
        print("Trad: {}".format(trade_score))

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
            decision = "draw_development"
        
        return decision, vertex, trade_get, trade_from


    def do_decision(self, player, decision, current_board, vertex, trade_get, trade_from):
        """
        Perform the decision
        """

        if trade_from != None and player.resources[trade_from] >= 4:
            player.resources[trade_from] -= 4 
            player.resources[trade_get] += 1

        if decision == "build_settlement":
            idx = vertex.name - 1
            distance = player.vertex_distances[idx]
            player.resources["wood"] = player.resources["wood"] - distance - 1
            player.resources["brick"] = player.resources["brick"] - distance - 1
            player.resources["wheat"] = player.resources["wheat"] - 1
            player.resources["sheep"] = player.resources["sheep"] - 1
            vertex.set_owner(player)
            player.points += 1
            return current_board

        elif decision == "build_city":
            idx = vertex.name - 1
            player.resources["wheat"] -= 2
            player.resources["stone"] -= 3
            vertex.is_city = True
            player.points += 1
            return current_board

        elif decision == "draw_development":
            current_board = self.draw_development_card(current_board, player)
            return current_board

        else: # "do_nothing"
            return current_board
    
    def calculate_city_scores(self, player, current_board):
        """
        Calculate the scores for placing a city.
        """

        # Get a list of the resources required
        resources = player.resources
        amounts = [resources["wheat"], resources["stone"]]

        # Initialize the scores to 0
        scores = [0 for vtx in current_board.vertices]

        # Ensure that there are at least 2 wheat and 3 stone
        if amounts[0] < 2 or amounts[1] < 3:
            return scores

        # Iterate over the player owned, non-city vertices
        for vtx in current_board.vertices:
            idx = vtx.name - 1
            costs = [2, 3]
            after = [amounts[i] - costs[i] for i in range(len(amounts))]

            # Skip empty vertex
            if vtx.owner is None:
                continue
            # Skip if it's already a city
            if vtx.is_city:
                continue

            scores[idx] = 0
            for tile_id in vtx.tile_id:
                tile_idx = tile_id - 1
                tile = current_board.tiles[tile_idx]
                tile_type = tile.get_tile_type()
                base_score = GameEngine.get_score(tile_type, player.strategy, tile)
                scores[idx] += base_score

        return scores
    
    def calculate_settlement_scores(self, player, current_board):
        """
        Calculate the scores for placing a settlement.
        """

        # Get a list of the resources required
        resources = player.resources
        amounts = [resources["wood"], resources["brick"], resources["wheat"], resources["sheep"]]
        
        # Initialize the scores to 0
        scores = [0 for vtx in current_board.vertices]

        # Ensure there are at least one of each resource
        if any(x == 0 for x in amounts):
            return scores
        
        # Iterate over every vertex, and determine the best spot for a settlement
        for vtx in current_board.vertices:
            idx = vtx.name - 1
            distance = player.vertex_distances[idx]
            costs = [distance + 1, distance + 1, 1, 1]
            after = [amounts[i] - costs[i] for i in range(len(amounts))]
            
            # Skip is the vertex is already owned
            if vtx.owner is not None:
                continue
            # Skip if the vertex has any direct neighbours
            if any([current_board.vertices[id - 1].owner is not None for id in vtx.neighbours]):
                continue
            # Skip if a required resource is negative after the purchase
            if any([x < 0 for x in after]):
                continue
            
            # Calculate the score based on tile type and strategy
            scores[idx] = (2 - distance) * 0.1
            for tile_id in vtx.tile_id:
                tile_idx = tile_id - 1
                tile = current_board.tiles[tile_idx]
                tile_type = tile.get_tile_type()
                base_score = GameEngine.get_score(tile_type, player.strategy, tile)
                scores[idx] += base_score # tile.probability
            
        return scores
    
    def calculate_development_score(self, player, current_board):
        """
        Calculate the score for choosing a development card this turn
        :param player: The player object who is deciding what to do
        :param current_board: The current state of the board
        :return: the score * the weight based on the player strategy
        """

        # Get a list of the resources required
        resources = player.resources
        amounts = [resources["sheep"], resources["stone"], resources["wheat"]]

        # Initialize the score to 0
        score = 0
        weight = 0.2

        # Ensure there are at least one of each resource
        if any(x == 0 for x in amounts):
            strategy = player.strategy
            return score

        if player.strategy == "development":
            weight = 1
        
        # Change score based on current number of knights
        if player.knights <= 3:
            score = 0.8
        else:
            score = GameEngine.translate(14 / player.knights, 0, 14/4, 0, 0.7)
        
        # Change score based on probability of victory points
        num_cards_left = len(current_board.development_deck) - player.knights - player.victory_point_cards - player.blank_cards
        if num_cards_left == 0:
            vp_probability = 0
        else:
            vp_probability = (5 - player.victory_point_cards) / num_cards_left

        score += vp_probability

        return score * weight

    def draw_development_card(self, current_board, player):
        """
        Draws a development card.
        """

        # Ensure there's at least one card in the deck
        if len(current_board.development_deck) < 1:
            return

        card = current_board.development_deck.pop(0)

        if card == "knight":
            player.knights += 1
            
        elif card == "victory_point":
            player.victory_point_cards += 1
            player.points += 1
        
        elif card == "blank":
            player.blank_cards += 1

        return current_board
    
    def calculate_trade_score(self, player, current_board):
        """
        Calculate the score for trading cards this turn
        :param player: The player object who is deciding what to do
        :param current_board: The current state of the board
        :return: the score * the weight based on the player strategy, trade_g: what the player gets, trade_f: what the player trades
        """

        score = 0
        weight = 0
        trade_g = None
        trade_f = None

        resources = player.resources
        strategy = player.strategy
        excess_resources, zero_resources = self.get_excess_and_zeros(resources)
        lowest_resource = self.get_lowest_resource(resources)

        if strategy == "settlements":
            if "stone" in excess_resources:
                trade_f = "stone"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "cities":
            if "wheat" not in excess_resources and "stone" not in excess_resources:
                random.shuffle(excess_resources)
                trade_f = excess_resources.pop(0)
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "sheep_monopoly":
            if "sheep" in excess_resources:
                trade_f = "sheep"
                weight = 1
                score = score + 1
                trade_g = lowest_resource
            
            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "wheat_monopoly":
            if "wheat" in excess_resources:
                trade_f = "wheat"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "stone_monopoly":
            if "stone" in excess_resources:
                trade_f = "stone"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "brick_monopoly":
            if "brick" in excess_resources:
                trade_f = "brick"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "wood_monopoly":
            if "wood" in excess_resources:
                trade_f = "wood"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        elif strategy == "development":
            if "brick" in excess_resources:
                trade_f = "brick"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif "wood" in excess_resources:
                trade_f = "wood"
                weight = 1
                score = score + 1
                trade_g = lowest_resource

            elif len(excess_resources) >= 1:
                weight, score, trade_g, trade_f = self.random_excess_for_lowest(excess_resources, lowest_resource)

        else:
            weight = 0

        return score*weight, trade_g, trade_f

    def get_excess_and_zeros(self, resources):
        """
        Get the resources that in excess of 4 or more and the resources at 0
        :param resources: Dictionary of resources of the player
        :return: List of resources in excess, and list of resources at zero
        """
        excess_resources = []
        zero_resources = []
        for key, value in resources.items():
            if value >= 4:
                excess_resources.append(key)

            elif value == 0:
                zero_resources.append(key)

        return excess_resources, zero_resources

    def get_lowest_resource(self, resources):
        lowest_resource = min(resources, key=resources.get)
        return lowest_resource

    def random_excess_for_lowest(self, excess_resources, lowest_resource):
        random.shuffle(excess_resources)
        trade_f = excess_resources.pop(0)
        weight = 0.75
        score = 1
        trade_g = lowest_resource

        return weight, score, trade_g, trade_f

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
                scores[vertex] += GameEngine.get_score(tile_type, strategy, current_board.tiles[tile-1])

        best_score = 0
        vertex_id = next(iter(scores))

        # find the best vertex for placement
        for key, value in scores.items():
            if value > best_score:
                best_score = value
                vertex_id = key

        return vertex_id.name

    @staticmethod
    def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    @staticmethod
    def get_tile_probability_weight(tile):
        """
        Gets the probability weight of the specified tile.
        """

        dice_value = tile.dice_value

        if dice_value == 0:
            return 0
        elif dice_value == 2 or dice_value == 12:
            return GameEngine.translate(1/36, 0, 5/36, 0, 1)
        elif dice_value == 3 or dice_value == 11:
            return GameEngine.translate(2/36, 0, 5/36, 0, 1)
        elif dice_value == 4 or dice_value == 10:
            return GameEngine.translate(3/36, 0, 5/36, 0, 1)
        elif dice_value == 5 or dice_value == 9:
            return GameEngine.translate(4/36, 0, 5/36, 0, 1)
        elif dice_value == 6 or dice_value == 8:
            return GameEngine.translate(5/36, 0, 5/36, 0, 1)

    @staticmethod
    def get_score(tile_type, strategy, tile):
        """
        :param tile_type: The type of the tile
        :param strategy: The strategy the player is using
        :return: The score the tile adds to the vertex
        """

        # weight_array: [stone, sheep, wood, brick, wheat]
        
        if strategy == "settlements":
            weight_array = [0.15,0.33,0.33,0.33,0.33]
        elif strategy == "cities":
            weight_array = [0.33,0.15,0.15,0.15,0.33]
        elif strategy == "stone_monopoly":
            weight_array = [0.33,0.15,0.15,0.15,0.15]
        elif strategy == "sheep_monopoly":
            weight_array = [0.15,0.33,0.15,0.15,0.15]
        elif strategy == "wood_monopoly":
            weight_array = [0.15,0.15,0.33,0.15,0.15]
        elif strategy == "brick_monopoly":
            weight_array = [0.15,0.15,0.15,0.33,0.15]
        elif strategy == "wheat_monopoly":
            weight_array = [0.15,0.15,0.15,0.15,0.33]
        elif strategy == "development":        
            weight_array = [0.33,0.33,0.15,0.15,0.33]
        else:
            weight_array = [0.33,0.33,0.33,0.33,0.33]
        
        score = GameEngine.determine_score(tile_type, weight_array)
        probability = GameEngine.get_tile_probability_weight(tile)
        return score * probability

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

    def evaluate_win(self, players):
        """
        Evaluate if a player has won
        :param players: The list of players playing
        :return: Winner
        """
        
        winner = None
        temp_points = 0

        for player in players:
            if player.knights >= 3:
                temp_points = temp_points + 2
            temp_points = temp_points + player.points

            if temp_points >= 10:
                winner = player
                # Add points for having knights
                player.points = player.points + 2

        return winner