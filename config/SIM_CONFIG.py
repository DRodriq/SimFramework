
######################################################
#                                                    #
#                   Configuration                    #
#                                                    #
######################################################

SIM_SPEED = .2
DO_POST_PROCESS = True
PAUSE_SIMULATION = 0
DO_RENDER = True

######################################################
#                                                    #
#                Simulation Settings                 #
#                                                    #
######################################################

VARIABLES = ["SIM_EXECUTION_SPEED", "..."]
NUM_GENERATIONS = 50000

######################################################
#                                                    #
#                Map Settings                        #
#                                                    #
######################################################

MAP_DIMENSION = 100
MAP_POINT_FEATURES = ["RESOURCE_TYPE", "RESOURCE_YIELD"]

######################################################
#                                                    #
#                Agent Settings                      #
#                                                    #
######################################################

NUM_INITIAL_AGENTS = 10
AGENT_STATS = []
AGENT_STARTING_SENSES = 2
AGENT_STARTING_ACTIONS = 2
AGENT_POSSIBLE_SENSES = ["SCORE", "SIZE", "SPEED","CROWD", "HOME_FIELD", "OPPONENT_RECORD", "COVERAGE"]
AGENT_POSSIBLE_ACTIONS = ["RUN", "JUMP", "SHOOT","STEAL", "BLOCK", "POST", "SCREEN", "WHEEL"]

######################################################
#                                                    #
#                Cortex Settings                     #
#                                                    #
######################################################

MINOR_MUTATION_DELTA = 10
MAJOR_MUTATION_RATE = [1,15]
EVOLUTION_RATE = [1, 900]

######################################################
#                                                    #
#                Neural Net Settings                 #
#                                                    #
######################################################

WEIGHT_RANGE = [900, 1000, 1000]
ODDS_OF_MUTATION = [1, 1000]
ODDS_OF_MAJOR_MUTATION = [1, 10]
WEIGHT_MUTATION_DELTA = 50 * (1/WEIGHT_RANGE[2])
SELECTION_MODE = "SEQUENTIAL"
