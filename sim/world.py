import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + "\\..")
from config import SIM_CONFIG as CFG
from random import randint

# A world is a 2D grid of map-points and a set of agents
class World:
    def __init__(self):
        self.cells = [[Cell(coordinates=(i,j)) for i in range(CFG.MAP_DIMENSION)] for j in range(CFG.MAP_DIMENSION)]

    def get_overlay(self, feature):
        overlay = [[cell.features.get(feature) for cell in row] for row in self.cells]
        return overlay
    
    def update_world(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].features[CFG.CELL_FEATURES[0]] = randint(0,1)

# A cell is a collection of attributes associated with an individual grid point and the ids of the present agents
"""
    Data model: 
        Cell()
            Feature - dict
                Key - static string
                Values - dynamic, any type
            Coordinates - Static tuple
            Agents - Dynamic list
"""
class Cell:
    def __init__(self, coordinates, features=None):
        self.coordinates = coordinates
        self.agents = []
        self.generate_random_features()

    def generate_random_features(self):
        val = randint(0,1)
        self.features = {i:val for i in CFG.CELL_FEATURES}


if __name__ == "__main__":

    test_world = World()

    print(test_world.cells[0][0].features)
    print(test_world.get_overlay(CFG.CELL_FEATURES[0]))