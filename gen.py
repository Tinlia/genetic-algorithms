import random 
import numpy as np
# A basic Genetic Algorithm Example using "The Builder's" amazing tutorial on Youtube

# Goal: Find the values of x, y, z that satisfy the equation foo(x,y,z) = 0
def foo(x,y,z):
    return 6*x**3 + 9*y**2 + 90*z - 25 # The goal is 25, so this will return the + or - error

# The function to determine fitness
def fitness(x, y, z):
    ans = foo(x,y,z)
    
    if ans == 0: # If the answer hits exactly 25, return a massive fitness
        return 9999
    else: # Else, return a higher fitness relative to how close the ans is to 0
        return abs(1/ans)
    
best_fitness_scores = [] # Save the best fitness scores for each generation
    
elitism = 4 # The number of best solutions to keep each generation
    
# Generate Solutions
solutions = []
for s in range(1000):
    # The x, y, z values cannot all be the same uniform random number, so we generate 3 random ones
    solutions.append( (random.uniform(0,10000), 
                       random.uniform(0,10000), 
                       random.uniform(0,10000)) )
    
generations = 10000 # 10,000 Generations
for i in range(generations):
    rankedsolutions = []
    for s in solutions:# We want to save both the fitness and the solution
        rankedsolutions.append( (fitness(s[0], s[1], s[2]), s) )
    rankedsolutions.sort(reverse=True)    
    
    # If the fitness is over a certain amount, we consider it to be good enough and stop
    if rankedsolutions[0][0] > 9999:
        print(f"=== Gen {i} best solutions ===")
        print(rankedsolutions[0])
        print("Solution found!")
        break
    
    # Selection based on fitness
    bestsolutions = rankedsolutions[:100]
    
    # solutions are formatted as such: (fitness, (x, y, z))
    
    elements_0 = [] # x values
    elements_1 = [] # y values
    elements_2 = [] # z values
    for s in bestsolutions:
        elements_0.append(s[1][0]) # Save the x
        elements_1.append(s[1][1]) # Save the y
        elements_2.append(s[1][2]) # Save the z
        
    newGen = []
    for i in range(elitism):
        newGen.append( (bestsolutions[i][1]))
    
    # Dynamic mutation rate
    mutation_rate = max(0.01, 1 - (i/generations)) # Ddecreases over time
    lb = 1 - (mutation_rate) # Lower bound
    ub = 1 + (mutation_rate) # Upper bound
    # Selection, Mutation, Crossover
    for _ in range((1000-elitism) // 2):  # We'll be adding two solutions per loop iteration
        # Select two parents from the best solutions
        parent1 = random.choice(bestsolutions)[1]
        parent2 = random.choice(bestsolutions)[1]

        # Perform crossover to generate two children
        child1 = (parent1[0], parent2[1], parent1[2])
        child2 = (parent2[0], parent1[1], parent2[2])

        # Mutate the children
        child1 = (child1[0] * random.uniform(lb, ub), child1[1] * random.uniform(lb, ub), child1[2] * random.uniform(lb, ub))
        child2 = (child2[0] * random.uniform(lb, ub), child2[1] * random.uniform(lb, ub), child2[2] * random.uniform(lb, ub))

        # Add the children to the new generation
        newGen.append(child1)
        newGen.append(child2)
    
    # Create the new population
    solutions = newGen