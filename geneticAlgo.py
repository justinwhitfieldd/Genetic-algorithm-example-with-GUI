import math
import random

def mathFunction(x, y):
    return (1-x)**2 * math.e ** (-x**2 -(y+1)**2) - (x - x**3 - y**3) * math.e**(-x**2 - y**2)

def binary_string_to_integer(value):
    val = int(value, 2) 
    max_value = 2

    for i in range(1, len(value)):
        max_value = 2 ** i + max_value

    scale = 6/(max_value - 1)
    scaled_val = float('{:.5f}'.format(val * scale - 3))
    return scaled_val

def mutations(chromosomes_after_crossover, Pm):
    list_chromosomes_after_crossover = list(chromosomes_after_crossover)
    for i in range(len(list_chromosomes_after_crossover)):
        for j in range(len(list_chromosomes_after_crossover[i])):
            list_chromosome = list(list_chromosomes_after_crossover[i])
            if random.random() < Pm:
                #print("MUTATION OCCURED")
                # print("val before mutation: ", chromosomes_after_crossover[i])
                bit = list_chromosome[j]
                if bit == "0":
                    list_chromosome[j] = "1"
                else:
                    list_chromosome[j] = "0"
                chromosomes_after_crossover[i] = ''.join(list_chromosome)

    return chromosomes_after_crossover

# creates a simulated roulette wheel by base 100 percentages for each value
# and stores in hash map with associated percentage
def roulette_wheel_creation(fitnessValues, N):
    roulette_percentage = [0] * N
    totalFitness = sum(f for f in fitnessValues if f > 0)
    roulette_percent_to_fitness_map = {}

    for i in range(len(fitnessValues)):
        if fitnessValues[i] > 0:
            roulette_percentage[i] = float('{:.5f}'.format((fitnessValues[i] / totalFitness) * 100))
        else:
            roulette_percentage[i] = 0.0
        roulette_percent_to_fitness_map[roulette_percentage[i]] = fitnessValues[i]

    roulette_percentage.sort(reverse=False)
    return roulette_percent_to_fitness_map, roulette_percentage

# selects an element from the roulette wheel by percentage
def roulette_wheel_selection(roulette_percentage):
    random_value = random.randrange(10000001) / 100000
    roulette_position = 0
    for i in range(len(roulette_percentage)):
        roulette_position += roulette_percentage[i]
        if roulette_position >= random_value:
            #print("Selected: ",roulette_percentage[i], " random num was :", random_value, " roulette position was: ",roulette_position)
            return roulette_percentage[i]
            break     

def crossover(binary_parent_strings, Pc):
    next_gen_chromosomes = []

    for i in range(len(binary_parent_strings)):
        cross_over_percent = random.randrange(1,11) / 10
        if cross_over_percent <= Pc:
            # no a-sexual reproduction here!
            potential_partners = binary_parent_strings[:i] + binary_parent_strings[i+1:]
            baby_daddy = potential_partners[random.randint(0,len(potential_partners)-1)]
            
            crossover_bit = random.randint(1,20) # all bits after this are swapped
         
            child_one = binary_parent_strings[i][:crossover_bit] + baby_daddy[crossover_bit:]
            child_two = baby_daddy[:crossover_bit] + binary_parent_strings[i][crossover_bit:]
            next_gen_chromosomes.append(child_one)
            next_gen_chromosomes.append(child_two)
        else:
            next_gen_chromosomes.append(binary_parent_strings[i])
    return next_gen_chromosomes

def initialize_chromosomes(N):
    chromosomes = []
    for i in range(N):
        chromosomeString = ""
        for j in range(20):
            m = random.randrange(2)
            chromosomeString += str(m)
        chromosomes.append(chromosomeString)
    return chromosomes

def run_training(N, Pc, Pm, epochs, ax):
    chromosomes = initialize_chromosomes(N)
    max_values = []
    for epoch in range(epochs):
        roulette_selected_chromosomes = []
        fitnessValues = [0] * N
        fitness_to_binary_map = {}
        #print(chromosomes)
        for i in range(N):
            #print(i)
            #print("chromosome sizes: ", len(chromosomes[i]))
            x_binary = chromosomes[i][:10]
            y_binary = chromosomes[i][10:20]
            x_float = [0] * N
            y_float = [0] * N
            x_float[i] = binary_string_to_integer(x_binary)
            y_float[i] = binary_string_to_integer(y_binary)
            fitness = mathFunction(x_float[i], y_float[i])
            #print("X: ",x_float[i]," Y: ",y_float[i]," fitness: ", fitness)
            fitness_to_binary_map[fitness] = chromosomes[i]
            fitnessValues[i] = fitness

        # select pair of chromosomes N times by roulette
        for i in range(N):
            roulette_percent_to_fitness_map, roulette_percentages = roulette_wheel_creation(fitnessValues, N)
            selected = roulette_wheel_selection(roulette_percentages)   
            roulette_selected_chromosomes.append(fitness_to_binary_map[roulette_percent_to_fitness_map[selected]])

        chromosomes_after_crossover = crossover(roulette_selected_chromosomes, Pc)
        chromosomes = mutations(chromosomes_after_crossover, Pm)
        max_value = max(fitnessValues) 
        max_values.append(max_value)
        print("EPOCH: ", epoch, " MAX VAL: ", max_value)

#uncomment this to run without gui
#run_training(10,0.7,0.004, 500, None)