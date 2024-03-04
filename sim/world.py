from config import SIM_CONFIG as CFG
import random
#import Agent

# A world is a 2D grid of map-points and a set of agents
class World:
    def __init__(self):
        self.map = [[MapPoint() for i in range(CFG.MAP_DIMENSION)] for j in range(CFG.MAP_DIMENSION)]
       # self.agents = [Agent.Agent() for i in range(CFG.NUM_INITIAL_AGENTS)]

    def get_overlay(self):
        return(list()) 

# A Landplot is a collection of attributes associated with an individual grid point and the ids of the present agents
class MapPoint:
    def __init__(self):
        self.agent_ids = []
        self.features = [{i:0 for i in CFG.MAP_POINT_FEATURES}]

def main():
    wrld = World()
    print(wrld.map[0][0].features)

main()