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
        self.read_vertices_file("vertices.txt")
	
    def read_vertices_file(self, file_name):
        vertices = []
        i = 0

        while (i < 54):
            vertices.append(Vertex(i + 1, None)) #TODO: add tile id
            i = i +1

        with open(file_name) as f:
            lines = f.readlines()
            l = []
            for x in lines:
                x = x.strip()
                if (len(x) > 0 and x[0] != "#"):
                    l = x.split(",")
                for y in l[1:len(l)]:
                    vertices[int(l[0]) - 1].add_neighbor(vertices[int(y) - 1])
        self.vertex_graph.add_vertices(vertices)
        print(str(self.vertex_graph.adjacencyList()))

    def populate_tile_vertex_map():
        self.tile_vertex_map[1] = [1]
        self.tile_vertex_map[2] = [1]
        self.tile_vertex_map[3] = [1,2]
        self.tile_vertex_map[4] = [
        self.tile_vertex_map[5] = [
        self.tile_vertex_map[6] = [
        self.tile_vertex_map[7] = [
        self.tile_vertex_map[8] = [
        self.tile_vertex_map[9] = [
        self.tile_vertex_map[10] = [
        self.tile_vertex_map[11] = [
        self.tile_vertex_map[12] = [
        self.tile_vertex_map[13] = [
        self.tile_vertex_map[14] = [
        self.tile_vertex_map[15] = [
        self.tile_vertex_map[16] = [
        self.tile_vertex_map[17] = [
        self.tile_vertex_map[18] = [
        self.tile_vertex_map[19] = [
        self.tile_vertex_map[20] = [
        self.tile_vertex_map[21] = [
        self.tile_vertex_map[22] = [
        self.tile_vertex_map[23] = [
        self.tile_vertex_map[24] = [
        self.tile_vertex_map[25] = [
        self.tile_vertex_map[26] = [
        self.tile_vertex_map[27] = [
        self.tile_vertex_map[28] = [
        self.tile_vertex_map[29] = [
        self.tile_vertex_map[30] = [
        self.tile_vertex_map[31] = [
        self.tile_vertex_map[32] = [
        self.tile_vertex_map[33] = [
        self.tile_vertex_map[34] = [
        self.tile_vertex_map[35] = [
        self.tile_vertex_map[36] = [
        self.tile_vertex_map[37] = [
        self.tile_vertex_map[38] = [
        self.tile_vertex_map[39] = [
        self.tile_vertex_map[40] = [
        self.tile_vertex_map[41] = [
        self.tile_vertex_map[42] = [
        self.tile_vertex_map[43] = [
        self.tile_vertex_map[44] = [
        self.tile_vertex_map[45] = [
        self.tile_vertex_map[46] = [
        self.tile_vertex_map[47] = [
        self.tile_vertex_map[48] = [
        self.tile_vertex_map[49] = [
        self.tile_vertex_map[50] = [
        self.tile_vertex_map[51] = [
        self.tile_vertex_map[52] = [
        self.tile_vertex_map[53] = [
        self.tile_vertex_map[54] = [
 

