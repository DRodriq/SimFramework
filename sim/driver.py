import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + "\\..")
from config import SIM_CONFIG as CFG 
import renderer
import simulation
import threading
import pygame
import time
import matplotlib.pyplot as plt

"""
    The entry point to the program
    Init and start simulation and renderer
    Establish post processing data and the data structures for them
    Run simulation loop, update renderer, log data
    Post process data
"""
def main():
    # Renderer setup
    rendering_thread = threading.Thread(target=renderer.start_rendering, daemon=None)
    if(CFG.DO_RENDER):
        print("[MAIN]: Starting Renderer")
        rendering_thread.start()
    time.sleep(1)

    # Data Structures
    print("[MAIN]: Initalizing Data Structures for Variables:", CFG.VARIABLES)
    results = [[0] for i in range(len(CFG.VARIABLES))]

    # Sim Init
    print("[MAIN]: Simulation Setup")
    sim = simulation.Simulation()

    # Loop 
    i = 0
    print("[MAIN]: Beginning Simulation Loop")
    while( i < CFG.NUM_GENERATIONS and rendering_thread.is_alive()):
        if(CFG.PAUSE_SIMULATION == 0):
            start = time.time()
            iter_results = sim.execute_timestep()
            for i in range(len(iter_results)):
                results[i+1].append(iter_results[i])
            end = time.time()
            results[0].append(end - start)
        if(CFG.DO_RENDER):
            overlays = sim.get_overlays()
            for i in range(len(overlays)):
                update = pygame.event.Event(renderer.GUI_CONFIG.OVERLAY_TYPES[i], message = overlays[i]) #Get object overlay
                pygame.event.post(update)

        #Collect Results
        time.sleep(CFG.SIM_SPEED)
        i = i + 1
    
    if(CFG.DO_POST_PROCESS):
        # Post Processing
        print("[MAIN]: Post-Processing", CFG.VARIABLES)
        for i in range(len(results)):
            plt.subplot(1,3,i+1)
            plt.title(CFG.VARIABLES[i])
            plt.plot(results[i], 'bo-')
        plt.show()

    # Teardown
    if(CFG.DO_RENDER):
        stop_rendering = pygame.event.Event(renderer.STOP_RENDERING, message=False)
        pygame.event.post(stop_rendering)
    print("[MAIN]: Done")


main()