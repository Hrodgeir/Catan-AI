class Player:
    def __init__(self, Id, strategy):
        self.id = Id
        self.strategy = strategy
        self.resources = {"sheep": 0, "brick": 0, "stone": 0, "wood": 0, "wheat": 0}

    def set_strategy(self, new_strategy):
        self.new_strategy = new_strategy

    def __repr__(self):
        return "(Name: " + str(self.id) + ", Strategy: " + str(self.strategy) + ")\n"
    
