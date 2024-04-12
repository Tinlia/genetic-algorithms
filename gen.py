import random 
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
    
# Generate Solutions
solutions = []
for s in range(1000):
    # The x, y, z values cannot all be the same uniform random number, so we generate 3 random ones
    solutions.append( (random.uniform(0,10000), 
                       random.uniform(0,10000), 
                       random.uniform(0,10000)) )
    
# 10,000 Generations
for i in range(10000):
    rankedsolutions = []
    for s in solutions:# We want to save both the fitness and the solution
        rankedsolutions.append( (fitness(s[0], s[1], s[2]), s) )
    rankedsolutions.sort(reverse=True)
    print(f"=== Gen {i} best solutions ===")
    print(rankedsolutions[0])
    
    # If the fitness is over a certain amount, we consider it to be good enough and stop
    if rankedsolutions[0][0] > 9999:
        print("Solution found!")
        break
    
    # Selection based on fitness
    bestsolutions = rankedsolutions[:100]
    
    elements_0 = [] # x values
    elements_1 = [] # y values
    elements_2 = [] # z values
    for s in bestsolutions:
        elements_0.append(s[1][0]) # Save the x
        elements_1.append(s[1][1]) # Save the y
        elements_2.append(s[1][2]) # Save the z
    
    newGen = []
    # Selection, Mutation, Crossover
    for _ in range(1000):
        # For each value, pick an element from the best solutions and change it by -1 -> 1%
        e1 = random.choice(elements_0) * random.uniform(0.99, 1.01)
        e2 = random.choice(elements_1) * random.uniform(0.99, 1.01)
        e3 = random.choice(elements_2) * random.uniform(0.99, 1.01)
        
        newGen.append( (e1, e2, e3) )
    
    # Create the new population
    solutions = newGen