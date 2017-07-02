from dock import *

class Vertex:
    def __init__(self, vertex, tile_id):
        self.name = vertex
        self.neighbors = []
        self.dock = None
        self.owner = None
        self.tile_id = tile_id
        
    def add_neighbor(self, neighbor):
        if isinstance(neighbor, Vertex):
            if neighbor.name not in self.neighbors:
                self.neighbors.append(neighbor.name)
                neighbor.neighbors.append(self.name)
                self.neighbors = sorted(self.neighbors)
                neighbor.neighbors = sorted(neighbor.neighbors)
        else:
            return False
        
    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            if isinstance(neighbor, Vertex):
                if neighbor.name not in self.neighbors:
                    self.neighbors.append(neighbor.name)
                    neighbor.neighbors.append(self.name)
                    self.neighbors = sorted(self.neighbors)
                    neighbor.neighbors = sorted(neighbor.neighbors)
            else:
                return False

    def set_dock(self, dock):
        if isinstance(dock, Dock):
            self.dock = dock
        
        else:
            return False

    #def __repr__(self):
        #return str(self.neighbors)
