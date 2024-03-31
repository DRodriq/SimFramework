from config import SIM_CONFIG as CFG 
from rendering import renderer
from sim import simulation
import threading
import pygame
import time
import matplotlib.pyplot as plt
from utils import logging

"""
    The entry point to the program
    Init and start simulation and renderer
    Establish post processing data and the data structures for them
    Run simulation loop, update renderer, log data
    Post process data
"""

class SimDriver():
    def __init__(self):
        logging.log("INFO", "Initializing sim driver", "driver.py", "driver.__init__")
        
        self.sim = simulation.Simulation()

        self.rendering_thread = threading.Thread(target=renderer.start_rendering, daemon=None)
        if(CFG.DO_RENDER):
            logging.log("INFO", "Driver starting renderer thread", "driver.py", "driver.__init__")
            self.rendering_thread.start()
        time.sleep(1)

        # Data Structures
        self.results = [[0] for i in range(len(CFG.VARIABLES))]
    
    def run(self):
        i = 0
        logging.log("MAIN", "Beginning Simulation Loop", "driver.py", "driver.run")
        while( i < CFG.NUM_GENERATIONS and self.rendering_thread.is_alive()):
            if(CFG.PAUSE_SIMULATION == 0):
                start = time.time()
                iter_results = self.sim.execute_timestep()
                for i in range(len(iter_results)):
                    self.results[i+1].append(iter_results[i])
                end = time.time()
                self.results[0].append(end - start)
                if(CFG.DO_RENDER):
                    overlays = self.sim.get_overlays()
                    for i in range(len(overlays)):
                        update = pygame.event.Event(renderer.GUI_CONFIG.OVERLAY_TYPES[i], message = overlays[i]) #Get object overlay
                        pygame.event.post(update)

            #Collect Results
            time.sleep(CFG.SIM_SPEED)
            i = i + 1

        # Teardown
        if(CFG.DO_RENDER):
            stop_rendering = pygame.event.Event(renderer.STOP_RENDERING, message=False)
            pygame.event.post(stop_rendering)
        logging.log("INFO", "Simulation loop end", "driver.py", "driver.run")


    def post_process(self):    
        if(CFG.DO_POST_PROCESS):
            # Post Processing
            print("[MAIN]: Post-Processing", CFG.VARIABLES)
            for i in range(len(self.results)):
                plt.subplot(1,3,i+1)
                plt.title(CFG.VARIABLES[i])
                plt.plot(self.results[i], 'bo-')
            plt.show()