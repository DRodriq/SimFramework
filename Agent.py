
import sys
from config import SIM_CONFIG
import DecisionCortex
import random

# An agent is a ### at a position in the world
class Agent:
    def __init__(self, id):
        self.ID = id
        self.cortex = DecisionCortex.DecisionCortex()


