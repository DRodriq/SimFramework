
from config import SIM_CONFIG as CFG
import random
import world

"""
    The simulation class is an interface with the simulated world
"""

class Simulation:
    def __init__(self):
        self.sim_world = world.World()

    def execute_timestep(self):
        #self.sim_world.set_agent_actions()
        #self.sim_world.update_world()

        # mocker
        results = []
        rand = random.randint(0,10)
        results.append(rand)
        return results

    def get_overlays(self):
        overlays = []
        overlays.append(self.sim_world)
        return overlays
