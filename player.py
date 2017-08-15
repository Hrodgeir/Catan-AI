import math
import random

class Player:
    """
    Object that represents a player in Catan
    """

    def __init__(self, Id, strategy):
        self.id = Id
        self.strategy = strategy
        self.resources = {"sheep": 0, "brick": 0, "stone": 0, "wood": 0, "wheat": 0}
        self.vertex_distances = []
        self.points = 2
        self.knights = 0
        self.victory_point_cards = 0
        self.num_settlements = 2
        self.decision = ""

    def set_strategy(self, new_strategy):
        self.new_strategy = new_strategy
        
    def update_distances(self, acquired_vertex, board):
        if self.vertex_distances == []:
            self.vertex_distances = [math.inf for v in board.vertices]
    
        acq_id = acquired_vertex.name - 1
        distances = board.vertex_distance_map[acq_id]
        
        for vtx in board.vertices:
            idx = vtx.name - 1
            if distances[idx] < self.vertex_distances[idx]:
                self.vertex_distances[idx] = distances[idx]

    @staticmethod
    def generate_strategies(num_of_strategies):
        """
        Generate a random order of strategies to give to the players
        :param num_of_stategies: The number of strategies to pick from
        :return: list of strategies
        """
        strategy_catalogue = ["cities", "settlements", "sheep_monopoly", "wheat_monopoly", "stone_monopoly", "brick_monopoly", "wood_monopoly", "development"]
        random.shuffle(strategy_catalogue)
        strategy_list = []

        for i in range(num_of_strategies):
            choice = strategy_catalogue.pop(0)
            strategy_list.append(choice)

        return strategy_list

    def __repr__(self):
        return "(Name: " + str(self.id) + ", Strategy: " + str(self.strategy) + ")\n"

    @staticmethod
    def read_strategies(num_of_stategies, file_name):
        """
        Read the strategies from a file
        :param num_of_strategies: The number of strategies to get
        :param file_name: the name of the file to read from
        """
        try:
            strategies = []
            with open(file_name) as f:
                lines = f.readlines()
                assert(len(lines) == num_of_stategies)
                for strategy in lines:
                    strategy = strategy.strip()
                    if (len(strategy)) > 0 and Player.valid_strategy(strategy):
                        strategies.append(strategy)
                    else:
                        raise ValueError

                return strategies
        
        except ValueError:
            print("Bad value in strategies.txt file...")
            raise

        except AssertionError:
            print("strategies.txt must have the same number of strategies as players...")
            raise

    @staticmethod
    def valid_strategy(strategy):
        """
        Ensure the strategy is valid
        :param strategy: String, The strategy to validate
        """
        strategy_catalogue = ["cities", "settlements", "sheep_monopoly", "wheat_monopoly", "stone_monopoly", "brick_monopoly", "wood_monopoly", "development"]
        retval = False
        
        if strategy in strategy_catalogue: 
            retval = True

        return retval