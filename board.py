""" Board Class """
import math
from dock import *
from tile import *
from vertex import *

class Board():
    """
    Represent the board as an Board object
    """
    def __init__(self, random=False):

        self.vertices = []
        self.vertex_distance_map = []
        self.tile_vertex_map = {}
        self.tile_by_dice_val = {"2":[],"3":[],"4":[],"5":[],"6":[],"7":[],"8":[],"9":[],"10":[],"11":[],"12":[]}
        self.populate_tile_vertex_map()
        
        if random:
            self.tiles = Tile.generate_layout()
            self.docks = Dock.generate_docks()

        else: 
            self.tiles = []
            self.docks = []
            self.read_tiles_file("tiles.txt")
            self.read_docks_file("docks.txt")
        
        for tile in self.tiles:
            if tile.dice_value != 0 and tile.tile_type != "desert":
                self.tile_by_dice_val[str(tile.dice_value)].append(tile.Id)
        
        self.read_vertices_file("vertices.txt")
        self.development_deck = Board.shuffle_deck() 
        self.populate_vertex_distance_map()
        self.current_roll = 0 
        self.player_state = []

    def read_vertices_file(self, file_name):
        """
        Read the vertices.txt file
        """

        i = 0

        # create the vertices
        while (i < 54):
            self.vertices.append(Vertex(i + 1, self.tile_vertex_map[i + 1])) #vertex name, surrounding tile ids
            i = i + 1
            
        self.populate_docks(self.vertices)

        # open vertices file to get the edges
        with open(file_name) as f:
            lines = f.readlines()
            l = []
            for line in lines:
                line = line.strip()
                if (len(line) > 0 and line[0] != "#"):
                    l = line.split(",")
                for y in l[1:len(l)]:
                    self.vertices[int(l[0]) - 1].neighbours.append(self.vertices[int(y) - 1].name) # draw edges accordingly   

    def valid_vertex_for_position(self, vertex_id):
        """
        Check to see if the position is available (enemies at least 2 edges away in board)
        """
        
        this_vertex = self.vertices[vertex_id]

        for neighbour in this_vertex.neighbours:
            neighbour_vertex = self.vertices[neighbour-1]
            if neighbour_vertex.owner != None:
               return False
        return True

    def read_tiles_file(self, file_name):
        with open(file_name) as f:
            lines = f.readlines()

            for x in lines:
                x = x.strip()
                if (len(x) > 0 and x[0] != "#"):
                    tile_info = x.split(",")
                    self.tiles.append(Tile(int(tile_info[0]), tile_info[1].lower(), tile_info[2], tile_info[3]))

    def read_docks_file(self, file_name):
        """
        Read in the dock order by resource
        :param file_name: The name of the file to read from
        """
        try:
            with open(file_name) as f:
                lines = f.readlines()
                assert(len(lines) == 10)
                for resource in lines: 
                    resource = resource.strip()
                    if (len(resource) > 0 and resource[0] != "#"):
                        if(self.validate_dock(resource)):
                            new_dock = Dock(resource)
                            self.docks.append(new_dock)
                        else:
                            raise ValueError

        except ValueError:
            print("Bad value in docks.txt file...")
            raise

        except AssertionError:
            print("docks.txt must have 10 lines only.")
            raise

    def get_available_vertices(self):
        """
        :return: all the available vertices the user can choose from
        """
        avail_vertices = []
        
        for vertex in self.vertices:
            if (self.valid_vertex_for_position(vertex.name - 1) and vertex.owner == None):
                avail_vertices.append(vertex)

        return avail_vertices

    def validate_dock(self, resource):
        """
        :param resource: The resource that was entered in the .txt
        :return: True or false whether or not the dock in docks.txt is valid
        """
        if (resource != "all" and resource != "wood" and resource != "wheat" and resource != "sheep" and resource != "brick" and resource != "stone"):
            return False
        else:
            return True

    @staticmethod
    def shuffle_deck():
        """
        Shuffle the development card deck
        """
        deck_catalogue =  {"knight" : 14, "victory_point": 5, "blank" : 6}
        deck_groups = [[type] * num for type, num in deck_catalogue.items()]
        deck = sum(deck_groups, [])

        deck = random.shuffle(deck)
        deck_stack = []

        ''' for i in range(25):
            deck_stack.append(deck.pop(0)) '''

        return deck

    def populate_docks(self, vertices):

        vertices[2].set_dock(self.docks[0])
        vertices[3].set_dock(self.docks[0])

        vertices[5].set_dock(self.docks[1])
        vertices[6].set_dock(self.docks[1])

        vertices[8].set_dock(self.docks[2])
        vertices[9].set_dock(self.docks[2])

        vertices[15].set_dock(self.docks[3])
        vertices[25].set_dock(self.docks[3])

        vertices[16].set_dock(self.docks[4])
        vertices[27].set_dock(self.docks[4])

        vertices[36].set_dock(self.docks[5])
        vertices[46].set_dock(self.docks[5])

        vertices[38].set_dock(self.docks[6])
        vertices[39].set_dock(self.docks[6])

        vertices[49].set_dock(self.docks[7])
        vertices[50].set_dock(self.docks[7])

        vertices[52].set_dock(self.docks[8])
        vertices[53].set_dock(self.docks[8])
                    
    def populate_tile_vertex_map(self):
        """
        Populates structure that shows which vertices are adjacent to which tiles
        """
        self.tile_vertex_map[1] = [1]
        self.tile_vertex_map[2] = [1]
        self.tile_vertex_map[3] = [1,2]
        self.tile_vertex_map[4] = [2]
        self.tile_vertex_map[5] = [2,3]
        self.tile_vertex_map[6] = [3]
        self.tile_vertex_map[7] = [3]
        self.tile_vertex_map[8] = [4]
        self.tile_vertex_map[9] = [1,4]
        self.tile_vertex_map[10] = [1,4,5]
        self.tile_vertex_map[11] = [1,2,5]
        self.tile_vertex_map[12] = [2,5,6]
        self.tile_vertex_map[13] = [2,3,6]
        self.tile_vertex_map[14] = [3,6,7]
        self.tile_vertex_map[15] = [3,7]
        self.tile_vertex_map[16] = [7]
        self.tile_vertex_map[17] = [8]
        self.tile_vertex_map[18] = [4,8]
        self.tile_vertex_map[19] = [4,8,9]
        self.tile_vertex_map[20] = [4,5,9]
        self.tile_vertex_map[21] = [5,9,10]
        self.tile_vertex_map[22] = [5,6,10]
        self.tile_vertex_map[23] = [6,10,11]
        self.tile_vertex_map[24] = [6,7,11]
        self.tile_vertex_map[25] = [7,11,12]
        self.tile_vertex_map[26] = [7,12]
        self.tile_vertex_map[27] = [12]
        self.tile_vertex_map[28] = [8]
        self.tile_vertex_map[29] = [8,13]
        self.tile_vertex_map[30] = [8,9,13]
        self.tile_vertex_map[31] = [9,13,14]
        self.tile_vertex_map[32] = [9,10,14]
        self.tile_vertex_map[33] = [10,14,15]
        self.tile_vertex_map[34] = [10,11,15]
        self.tile_vertex_map[35] = [11,15,16]
        self.tile_vertex_map[36] = [11,12,16]
        self.tile_vertex_map[37] = [12,16]
        self.tile_vertex_map[38] = [12]
        self.tile_vertex_map[39] = [13]
        self.tile_vertex_map[40] = [13,17]
        self.tile_vertex_map[41] = [13,14,17]
        self.tile_vertex_map[42] = [14,17,18]
        self.tile_vertex_map[43] = [14,15,18]
        self.tile_vertex_map[44] = [15,18,19]
        self.tile_vertex_map[45] = [15,16,19]
        self.tile_vertex_map[46] = [16,19]
        self.tile_vertex_map[47] = [16]
        self.tile_vertex_map[48] = [17]
        self.tile_vertex_map[49] = [17]
        self.tile_vertex_map[50] = [17,18]
        self.tile_vertex_map[51] = [18]
        self.tile_vertex_map[52] = [18,19]
        self.tile_vertex_map[53] = [19]
        self.tile_vertex_map[54] = [19]
        
    def populate_vertex_distance_map(self):
        self.vertex_distance_map = [None for v in self.vertices]
        
        #dijkstra's Algorithm
        for vtx in self.vertices:
            idx = vtx.name - 1
            
            distances = [math.inf for v in self.vertices]
            distances[idx] = 0
            
            visited = [False for v in self.vertices]
            unvisited = [vtx]
            
            while unvisited:
                current = unvisited.pop(0)
                c_idx = current.name - 1
                visited[c_idx] = True
                
                neighbor_distance = distances[c_idx] + 1
                for neighbor in current.neighbours:
                    n_idx = neighbor - 1
                    if neighbor_distance < distances[n_idx]:
                        distances[n_idx] = neighbor_distance
                    
                    if not visited[n_idx]:
                        unvisited.append(self.vertices[n_idx])
            
            self.vertex_distance_map[idx] = distances

    def __repr__(self):
        output_vertices = ""
        for vertex in self.vertices:
            output_vertices += vertex.__repr__()

        return output_vertices + "\n"