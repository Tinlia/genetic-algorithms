import random

POPULATION_SIZE = 1000
MUTATION_RATE = 0.9
CROSSOVER_RATE = 0.8
ELITISM = 100
GENERATIONS = 1000
GENE_LENGTH = 100
FITNESS_CUTOFF = 9999

def foo(gene):
    return sum(gene)

def fitness(gene):
    ans = foo(gene)
    
    if ans == GENE_LENGTH:
        return FITNESS_CUTOFF
    else:
        return ans
    
# Generate Solutions
solutions = []
for s in range(POPULATION_SIZE):
    solutions.append( [random.randint(0, 1) for _ in range(GENE_LENGTH)] )

for i in range(GENERATIONS):
    rankedsolutions = []
    for s in solutions:
        rankedsolutions.append( (fitness(s), s) )
    rankedsolutions.sort(reverse=True)
    
    if rankedsolutions[0][0] >= FITNESS_CUTOFF:
        print(f"=== Gen {i} best solutions ===")
        print(rankedsolutions[0])
        print("Solution found!")
        break
    
    bestsolutions = rankedsolutions[:ELITISM]
        
    newGen = []
    for i in range(ELITISM):
        newGen.append( bestsolutions[i][1])
    
    for _ in range((POPULATION_SIZE-ELITISM) // 2):
        parent1 = random.choice(bestsolutions)[1]
        parent2 = random.choice(bestsolutions)[1]

        if random.random() < CROSSOVER_RATE:
            crossover_point = random.randint(0, GENE_LENGTH)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
        else:
            child1 = parent1
            child2 = parent2

        if random.random() < MUTATION_RATE:
            mutation_point = random.randint(0, GENE_LENGTH-1)
            child1[mutation_point] = 1 - child1[mutation_point]
            child2[mutation_point] = 1 - child2[mutation_point]

        newGen.append(child1)
        newGen.append(child2)
    
    solutions = newGen
