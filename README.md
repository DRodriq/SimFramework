## About ##

CONFIG.py is a collection of global variables accessed by one or more files
    - Screen sizing
    - Simulation speed
    - Renderer colors and drawing settings
    - Dynamic variables that need to be accessed by multiple threads such as PAUSE
    - Entity specific definitions

Driver.py is the main entry point into the program
    - Starts Renderer
    - Initializes any data structures desired for collection and post-processing
    - Initializes the simulation
    - Runs the simulation loop
    - Post-processes results
    - Cleanup

Simulation.py is the simulation class
    - Simulations are a set of entities and the rules and processes to perform on them
    - Simulations always run by single timestep
    - The implementation of the simulation and the entites included is application specific

Entity classes are any objects that we want to include in the simulation
    - Examples include agents and a collection of MapPoints we want to organize into a map
    - Instances of entities will be organized in a simulation and operations will be performed on them
    - Entities are application specific, their structure, definitions, and rules are on a case-by-case basis
