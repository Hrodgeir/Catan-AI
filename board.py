""" Board Class """
import placement
from graph import *
from vertex import *

class Board():
    def __init__(self, tiles):
        self.placements = []
        self.vertex_graph = Graph()
        self.tile_vertex_map = {}

        #for i in range(54):
            #self.placements.append(placement.Placement(None, None, None))

        """ How to generate board? """
        #i would say just read from an input file.
        self.populate_tile_vertex_map()
        self.read_vertices_file("vertices.txt")
	
    def read_vertices_file(self, file_name):
        vertices = []
        i = 0

        # create the vertices
        while (i < 54):
            vertices.append(Vertex(i + 1, self.tile_vertex_map[i + 1])) #vertex name, sorrounding tile ids
            i = i + 1

        # open vertices file to get the edges
        with open(file_name) as f:
            lines = f.readlines()
            l = []
            for x in lines:
                x = x.strip()
                if (len(x) > 0 and x[0] != "#"):
                    l = x.split(",")
                for y in l[1:len(l)]:
                    vertices[int(l[0]) - 1].add_neighbor(vertices[int(y) - 1]) # draw edges accordingly
        self.vertex_graph.add_vertices(vertices) # store graph
        #print(str(self.vertex_graph.adjacencyList()))

    # check to see if the position is available (enemies at least 2 edges away in board)
    def valid_vertex_for_position(vertex_id):
        for x in self.vertex_graph.vertices[vertex_id]:
            print(x.name)
            if (x.owner != None):
                return False
        return True
    
    # populates structure that shows which vertices are adjecent to which tiles
    def populate_tile_vertex_map(self):
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
 

