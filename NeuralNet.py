import numpy as np
import random
from config import SIM_CONFIG

class NeuralNetwork:
    def __init__(self, inputs, outputs):
        self.decision_cortex = []
        self.num_inputs = len(inputs)
        self.num_outputs = len(outputs)
        self.inputs = inputs
        self.outputs = outputs
        self.num_hidden_layers = self.calculate_num_hidden_layers
        self.num_nodes_per_layer = self.calculate_nodes_per_layer()
        self.create_input_matrices()
        self.generate_new_cortex()

    def create_input_matrices(self):
        self.decision_cortex.append(np.identity(self.num_inputs))

    def generate_new_cortex(self):
        for i in range(self.num_hidden_layers):
            dimension = self.num_nodes_per_layer[i]
            self.create_hidden_layer_matrix(dimension=dimension)
        self.create_output_matrix()

    def calculate_num_hidden_layers(self):
        total_io = self.num_inputs + self.num_outputs
        if(total_io % 2 == 1):
            total_io = total_io + 1
        max_hidden_layers = (total_io / 2) - 1
        num_layers = random.randint(0,max_hidden_layers)
        return num_layers
    
    def calculate_nodes_per_layer(self):
        nodes_per_layer = [0 for i in range(self.num_hidden_layers)]
        for i in range(len(nodes_per_layer)):
            num_nodes = random.randint(1,self.num_hidden_layers)
            nodes_per_layer[i] = num_nodes
        return nodes_per_layer

    def create_output_matrix(self):
        dimension1 = self.decision_cortex[-1].shape[1]
        dimension2 = len(self.num_outputs)
        matrix = np.identity((dimension1, dimension2))
        self.decision_cortex.append(matrix)

    def create_hidden_layer_matrix(self, dimension):
        # Create an n-dimensional square array filled with zeros
        matrix = np.zeros((self.decision_cortex[-1].shape[1] ,dimension))
        # Fill the array with random values between
        for i in range(self.decision_cortex[-1].shape[1]):
            for j in range(dimension):
                    matrix[i, j] = (random.randint(SIM_CONFIG.WEIGHT_RANGE, SIM_CONFIG.WEIGHT_RANGE) / SIM_CONFIG.WEIGHT_RANGE[2])
        self.decision_cortex.append(matrix)

    def get_decision(self, input_vector):
        if(input_vector == ["TEST"]):
            random_output = random.randint(0, len(self.available_outputs) - 1)
            return(self.outputs[random_output])
        if(len(input_vector) == self.num_inputs):
            current_vector = input_vector
            for i in range(len(self.decision_cortex)):
                current_vector = np.matmul(current_vector,self.decision_cortex[i])
            largest_pulse = 0
            index = -1
            for i in range(len(current_vector)):
                if(current_vector[i] > largest_pulse):
                    current_vector[i] = largest_pulse
                    index = i
            return(self.outputs[index])
        print("[ERROR][input_vector][input_matrix] " + input_vector + " applied to matrix " + self.decision_cortex[0])
        random_output = random.randint(0, self.num_outputs - 1)
        return(self.outputs[random_output])

    def mutate(self):
        #Major mutation or just minor?
        dice = random.randint(SIM_CONFIG.ODDS_OF_MAJOR_MUTATION[0], SIM_CONFIG.ODDS_OF_MAJOR_MUTATION[1])
        if(dice == SIM_CONFIG.ODDS_OF_MAJOR_MUTATION[0]):
            self.major_mutation()
        self.minor_mutation()

    def major_mutation(self):
        all_inputs_assigned = False
        all_outputs_assigned = False
        if(len(self.inputs) == len(SIM_CONFIG.AGENT_POSSIBLE_SENSES)):
            all_inputs_assigned = True
        if(len(self.inputs) == len(SIM_CONFIG.AGENT_POSSIBLE_SENSES)):
            all_outputs_assigned = True
        if(not(all_inputs_assigned) and not(all_outputs_assigned)):
            dice = random.randint(0,1)
        if(all_inputs_assigned and not(all_outputs_assigned)):
            dice = 1
        if(not(all_inputs_assigned) and all_outputs_assigned):
            dice = 0
        if(dice == 0):
            if(SIM_CONFIG.SELECTION_MODE == "SEQUENTIAL"):
                new_input = SIM_CONFIG.AGENT_POSSIBLE_SENSES[len(self.inputs)]
                self.inputs.append(new_input)
                self.create_input_matrices()
        if(dice == 1):
            if(SIM_CONFIG.SELECTION_MODE == "SEQUENTIAL"):
                new_output = SIM_CONFIG.AGENT_POSSIBLE_SENSES[len(self.outputs)]
                self.outputs.append(new_output)
                self.create_output_matrix()

    def minor_mutation(self):
        #Could lead to creation of new hidden layer or just creation of new nodes
        new_num_hidden_layers = self.calculate_num_hidden_layers()
        if(new_num_hidden_layers != self.num_hidden_layers):


# Need to create a base neural net with n inputs and m outputs
# Need to create h hidden layers with w nodes
# When an agent's offspring evolves, need to take the parent matrix and add either 1 input or output and reshape
        