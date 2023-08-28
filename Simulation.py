
from config import SIM_CONFIG as CFG
import random
import World

"""
    The simulation class holds a list of entities and performs operations on and with the entities
"""

class Simulation:
    def __init__(self):
        self.world = [[0 for i in range(CFG.MAP_DIMENSION)] for j in range(CFG.MAP_DIMENSION)]
        print(self.world)

    def initialize(self):
        self.initialize_map()

    def initialize_map(self):
        for i in range(0, CFG.MAP_DIMENSION):
            for j in range(0, CFG.MAP_DIMENSION):
                self.world[j][i] = random.randint(0,1)
    
    # Provide information about the world and have agent's execute their turn, then update the world accordingly
    def execute_timestep(self):
        results = []
        rand = random.randint(0,10)
        results.append(rand)
        return results

    def get_overlays(self):
        overlays = []
        overlays.append(self.world)
        return overlays
