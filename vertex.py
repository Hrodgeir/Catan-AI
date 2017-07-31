from dock import *

class Vertex:
    def __init__(self, vertex, tile_id):
        self.name = vertex
        self.neighbours = []
        self.my_dock = None
        self.owner = None
        self.tile_id = tile_id

    def set_dock(self, new_dock):
        """
        Set the connected dock type for the vertex
        :param new_dock: Dock object 
        """
        if isinstance(new_dock, Dock):
            self.my_dock = new_dock
        else:
            return False     

    def set_owner(self, new_owner):
        """
        Set the owner for the vertex if it is not owned
        :param new_owner: Player object 
        """
        if self.owner is None: 
            self.owner = new_owner
        else:
            print("This vertex already has an owner: " + self.__repr__())    

    def __repr__(self):
        return "Vertex: " + str(self.name) + ", Owner: " + self.owner.__repr__() + " , Neighbours: " + str(self.neighbours) + "\n"
