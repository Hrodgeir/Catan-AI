from dock import *

class Vertex:
    def __init__(self, vertex, tile_id):
        self.name = vertex
        self.neighbours = []
        self.dock = None
        self.owner = None
        self.tile_id = tile_id

    def set_dock(self, dock):
        if isinstance(dock, Dock):
            self.dock = dock
        
        else:
            return False            

    def __repr__(self):
        return "Name: " + str(self.name) + ", Owner: " + self.owner + " ,Neighbours: " + str(self.neighbours) + "\n"
