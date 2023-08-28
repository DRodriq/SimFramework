import random
from config import SIM_CONFIG

class DecisionCortex:
    def __init__(self):
        self.cortex = [[0 for i in range(SIM_CONFIG.AGENT_STARTING_SENSES+1)] for j in range(SIM_CONFIG.AGENT_STARTING_ACTIONS)]
        self.inputs = []
        for i in range(SIM_CONFIG.AGENT_STARTING_SENSES):
            self.inputs.append(SIM_CONFIG.AGENT_POSSIBLE_SENSES[i])
        self.outputs = []
        for i in range(SIM_CONFIG.AGENT_STARTING_ACTIONS):
            self.outputs.append(SIM_CONFIG.AGENT_POSSIBLE_ACTIONS[i])
        self.num_rules = self.calculate_num_rules()
        self.rules = []
        self.generate_rules()

    def calculate_num_rules(self):
        max_num = (len(self.cortex) * len(self.cortex[0]))
        min_num = max_num / 2 if max_num % 2 == 0 else ((max_num + 1)/2)
        num_rules = random.randint(min_num,max_num)
        return num_rules
    
    def generate_rules(self):
        for i in range(self.num_rules):
            self.add_random_rule()

    def add_random_rule(self):
        origin = [random.randint(0, len(self.cortex)-1), random.randint(1,len(self.cortex[0])-1)]
        dest = [random.randint(0, len(self.cortex)-1), random.randint(1,len(self.cortex[0])-1)]
        weight = float(random.randint(SIM_CONFIG.WEIGHT_RANGE[0],SIM_CONFIG.WEIGHT_RANGE[1]) / SIM_CONFIG.WEIGHT_RANGE[2])
        rule = [origin, dest, weight]
        self.rules.append(rule)

    def get_decision(self, input_vector):
        input_vector = normalize_vector(input_vector)
        if(len(input_vector) != len(self.inputs)):
            print("[ERROR] INPUT VECTOR DOES NOT MATCH LENGTH OF INPUTS!")
        for i in range(len(self.cortex)):
            for j in range(1, len(self.cortex[i])):
                self.cortex[i][j] = input_vector[j-1]
        for i in range(len(self.rules)):
            origin = self.rules[i][0]
            origin_value = self.cortex[origin[0]][origin[1]]
            dest = self.rules[i][1]
            dest_value = self.cortex[dest[0]][dest[1]]
            weight = self.rules[i][2]
            dest_value = float(dest_value) * float(weight * origin_value)
            self.cortex[dest[0]][dest[1]] = dest_value
        highest_impulse = -100000
        highest_impulse_index = -1
        for i in range(len(self.cortex)):
            for j in range(1,len(self.cortex[i])):
                self.cortex[i][0] = self.cortex[i][0] + self.cortex[i][j]
            if(self.cortex[i][0] > highest_impulse):
                highest_impulse = self.cortex[i][0]
                highest_impulse_index = i
        self.cortex = [[0 for i in range(len(self.inputs)+1)] for j in range(len(self.outputs))]
        if(highest_impulse_index != -1):
            return self.outputs[highest_impulse_index]

    def mutate(self):
        #major or minor mutation?
        dice = random.randint(SIM_CONFIG.EVOLUTION_RATE[0], SIM_CONFIG.EVOLUTION_RATE[1])
        if(dice == SIM_CONFIG.EVOLUTION_RATE[0]):
            self.evolve()
            self.major_mutation()
        dice = random.randint(SIM_CONFIG.MAJOR_MUTATION_RATE[0], SIM_CONFIG.MAJOR_MUTATION_RATE[1])
        if(dice == SIM_CONFIG.MAJOR_MUTATION_RATE[0]):
            self.major_mutation()
        self.minor_mutation()

    def major_mutation(self):
        print("[LOG] MAJOR MUTATION!")
        max_rules = (len(self.inputs) * len(self.outputs))
        min_rules = max_rules / 2 if max_rules % 2 == 0 else ((max_rules + 1) / 2) 
        delta_high = max_rules - self.num_rules
        delta_low = (self.num_rules - min_rules) * -1
        rules_to_add = random.randint(delta_low, delta_high)
        if(rules_to_add > 0):
            for i in range(rules_to_add):
                self.add_random_rule()
                self.num_rules = self.num_rules + 1
        if(rules_to_add < 0):
            for i in range(0, (-1*rules_to_add)):
                index_to_remove = random.randint(0, self.num_rules-1)
                self.rules.pop(index_to_remove)
                self.num_rules = self.num_rules - 1

    def minor_mutation(self):
        for i in range(0, len(self.rules)):
            delta = float(random.randint(-1*SIM_CONFIG.MINOR_MUTATION_DELTA, SIM_CONFIG.MINOR_MUTATION_DELTA) / 1000)
            self.rules[i][2] = self.rules[i][2] + delta

    def evolve(self):
        print("EVOLUTION!")
        all_inputs_assigned = False
        all_outputs_assigned = False
        if(len(self.inputs) == len(SIM_CONFIG.AGENT_POSSIBLE_SENSES)):
            all_inputs_assigned = True
        if(len(self.inputs) == len(SIM_CONFIG.AGENT_POSSIBLE_SENSES)):
            all_outputs_assigned = True
        if(not(all_inputs_assigned) and not(all_outputs_assigned)):
            dice = random.randint(0,1)
        else:
            print("[LOG] All senses and actions assigned to this agent!")
            return
        if(all_inputs_assigned and not(all_outputs_assigned)):
            dice = 1
        if(not(all_inputs_assigned) and all_outputs_assigned):
            dice = 0   
        if(dice == 0): # add input
            if(SIM_CONFIG.SELECTION_MODE == "SEQUENTIAL"):
                self.inputs.append(SIM_CONFIG.AGENT_POSSIBLE_SENSES[len(self.inputs) -len(SIM_CONFIG.AGENT_POSSIBLE_SENSES)])
                for i in range(len(self.cortex)):
                    self.cortex[i].append(0)
        if(dice == 1): # add output
            if(SIM_CONFIG.SELECTION_MODE == "SEQUENTIAL"):
                self.outputs.append(SIM_CONFIG.AGENT_POSSIBLE_ACTIONS[len(self.outputs) - len(SIM_CONFIG.AGENT_POSSIBLE_ACTIONS)])
                self.cortex.append([0 for i in range(len(self.inputs)+1)])


def normalize_vector(vector):
    max_value = -1000000
    min_value = 100000
    if(len(vector) == 1):
        return [1]
    if(len(vector) == 2 and vector[0] == vector[1]):
        return [1,1]
    for i in range(len(vector)):
        if(vector[i] > max_value):
            max_value = vector[i]
        if(vector[i] < min_value):
            min_value = vector[i]
    for i in range(len(vector)):
        vector[i] = float((vector[i] - min_value) / (max_value - min_value)) + .01
    return(vector)



def test():
    decision_cortex = DecisionCortex()
    output_counters = [0 for i in range(len(SIM_CONFIG.AGENT_POSSIBLE_ACTIONS))]
    for i in range(SIM_CONFIG.NUM_GENERATIONS):
        print(str(i) +": ")
        input_vector = []
        for i in range(len(decision_cortex.inputs)):
            input_vector.append(random.randint(1,100))
        decision = decision_cortex.get_decision(input_vector)
        for i in range(len(SIM_CONFIG.AGENT_POSSIBLE_ACTIONS)):
            if(decision == SIM_CONFIG.AGENT_POSSIBLE_ACTIONS[i]):
                output_counters[i] = output_counters[i] + 1
        print(decision)
        decision_cortex.mutate()
    print(output_counters)
    print(decision_cortex.inputs)
    print(decision_cortex.outputs)

test()