import random
# Hyperparameters
# Modified hyperparameters for better exploration
POPULATION_SIZE = 1000
GENERATIONS = 500
MUTATION_RATE = 0.5
MUTATION_CHANCE = 0.3  # Reduced to prevent too much disruption
CROSSOVER_RATE = 0.7  # Increased to promote more exploration
REPLICATION_RATE = 0.2  # Reduced elite preservation
TOURNAMENT_SIZE = 10  # For tournament selection

OPERATORS = ['+', '-', '*', '/']
VARIABLES = ['x', 'y', 'z']
CUTOFF_FITNESS = 31000     # The fitness at which we consider the solution found
MAX_HEIGHT = 8              # The maximum depth of the tree (A higher number might require increasing Python's limit)

goal = 574.7149963378906 # Next minute's open price
x = 506.6820068359375 # Open 
y = 500.7799987792969 # High
z = 530.6700134277344 # Low

# TEST PARAMETERS
print_method_names = False
print_solution_sizes = False

class Node:
    def __init__(self, value=None, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

class Tree:
    def __init__(self, root=Node(value=random.choice(OPERATORS))):
        self.root = root
        self.size = 1
        self.height = 1

# Method to calculate the value of a tree
def foo(root):
    if print_method_names: print("Foo")
    if root is None:
        return 0  # Return a default value if the node is None

    if root.value == '+':
        left_val = foo(root.left)
        right_val = foo(root.right)
        return left_val + right_val if left_val is not None and right_val is not None else 0
    elif root.value == '-':
        left_val = foo(root.left)
        right_val = foo(root.right)
        return left_val - right_val if left_val is not None and right_val is not None else 0
    elif root.value == '*':
        left_val = foo(root.left)
        right_val = foo(root.right)
        return left_val * right_val if left_val is not None and right_val is not None else 0
    elif root.value == '/':
        left_val = foo(root.left)
        right_val = foo(root.right)
        return left_val / right_val if left_val is not None and right_val != 0 else 0
    else:
        if root.value == 'x':
            return x
        elif root.value == 'y':
            return y
        else:
            return z

def fitness(root):
    if print_method_names: print("Fitness")
    if root is None:
        return 0  # Return a default fitness if the tree is None

    ans = abs(foo(root) - goal)

    if ans == 0:
        return CUTOFF_FITNESS
    else:
        return abs(1 / ans)

def tournament_selection(ranked_solutions, tournament_size):
    """Tournament selection for better parent selection"""
    tournament = random.sample(ranked_solutions, tournament_size)
    return max(tournament, key=lambda x: x[0])[1]

# Method to perform crossover between two trees
def crossover(parent1, parent2):
    """Enhanced crossover that can swap any subtree"""
    tree1 = Tree(clone(parent1.root))
    tree2 = Tree(clone(parent2.root))
    
    # Get all nodes from both trees
    nodes1 = []
    nodes2 = []
    
    def collect_nodes(root, nodes):
        if root:
            nodes.append(root)
            collect_nodes(root.left, nodes)
            collect_nodes(root.right, nodes)
    
    collect_nodes(tree1.root, nodes1)
    collect_nodes(tree2.root, nodes2)
    
    if not nodes1 or not nodes2:
        return tree1, tree2
    
    # Randomly select crossover points
    node1 = random.choice(nodes1)
    node2 = random.choice(nodes2)
    
    # Randomly choose whether to swap left or right subtree
    if random.random() < 0.5:
        temp = node1.left
        node1.left = node2.left
        node2.left = temp
    else:
        temp = node1.right
        node1.right = node2.right
        node2.right = temp
    
    return tree1, tree2

def get_random_node(root):
    def traverse(root):
        if root is not None:
            nodes.append(root)
            traverse(root.left)
            traverse(root.right)
    
    if root is None:
        return None

    nodes = []
    # stack = [root]

    # # Traverse the tree using a stack
    # while stack:
    #     node = stack.pop()
    #     nodes.append(node)

    #     if node.left:
    #         stack.append(node.left)
    #     if node.right:
    #         stack.append(node.right)
    
    traverse(root)

    # Randomly select a node from the list of nodes
    return random.choice(nodes)

# Helper method to check and adjust the height of a tree while returning the new size
def adjust_tree(tree, node, depth=1):
    if print_method_names: print("Adjust Tree")
    # print("Adjusting tree with depth", depth)
    
    if node is None:
        return 0
    
    # print("Node.left = ", node.left, " | Node.right = ", node.right)
    # If the current depth is one less than the max height, add a terminal node and return the new size
    if depth >= MAX_HEIGHT-1:
        tree.height = depth
        node.left = Node(value=random.choice(VARIABLES))
        node.right = Node(value=random.choice(VARIABLES))
        # print("Returning 3")
        return 3 # The current node, the left node, and the right node
    
    # If the current depth is greater than the tree's current height, update the height
    if depth > tree.height:
        tree.height = depth
        
    # If the current depth is not the max height, continue to traverse the tree 
    
    # If at the end of a subtree, return 1
    if node.left is None and node.right is None:
        # print("Returning 1")
        return 1
    
    # Otherwise, continue to traverse the tree
    else:    
        return adjust_tree(tree, node.left, depth+1) + adjust_tree(tree, node.right, depth+1)
   

# Helper method to clone a tree
def clone(root):
    if print_method_names: print("Clone")
    if root is None:
        return None
    
    # Create a new node with the same value
    new_node = Node(root.value)
    
    # Recursively clone left and right subtrees
    new_node.left = clone(root.left)
    new_node.right = clone(root.right)
    
    return new_node
      
# TODO: Method to traverse a binary tree
def mutate(node, depth=0):
    """Enhanced mutation that can modify structure and variables"""
    if node is None:
        return node
    
    if random.random() < MUTATION_CHANCE:
        # Different mutation types
        mutation_type = random.random()
        
        if mutation_type < 0.3:  # Change operator/variable
            if node.value in OPERATORS:
                node.value = random.choice(OPERATORS)
            elif node.value in VARIABLES:
                node.value = random.choice(VARIABLES)
                
        elif mutation_type < 0.5 and depth < MAX_HEIGHT - 1:  # Grow subtree
            if node.value in VARIABLES:
                node.value = random.choice(OPERATORS)
                node.left = Node(value=random.choice(VARIABLES))
                node.right = Node(value=random.choice(VARIABLES))
                
        elif mutation_type < 0.7:  # Prune subtree
            if node.value in OPERATORS:
                node.value = random.choice(VARIABLES)
                node.left = None
                node.right = None
    
    if node.left:
        node.left = mutate(node.left, depth + 1)
    if node.right:
        node.right = mutate(node.right, depth + 1)
    
    return node      
        
# Method to print the equation from a tree
def build_string(node):
    if print_method_names: print("Build String")
    if node is None:
        return "0"

    left_str = build_string(node.left)
    right_str = build_string(node.right)

    # Check if the node is a variable or operator
    if node.value in VARIABLES:
        return node.value
    elif node.value in OPERATORS:
        # Check if left and right subtrees are present
        if left_str and right_str:
            return f"({left_str} {node.value} {right_str})"
        elif left_str:
            return f"({left_str} {node.value})"
        elif right_str:
            return f"{node.value} {right_str}"

    return ""

# Helper method to build a solution tree
def build_tree(tree, node, height=1):
    if print_method_names: print("Build Tree")
    if node == None:
        print("Node is None")
        return
    
    if height >= MAX_HEIGHT:
        node.left = Node(value=random.choice(VARIABLES))
        node.right = Node(value=random.choice(VARIABLES))
        tree.size += 2
        return
    
    # Guarantee a decent tree size
    if tree.size < 8:
        node.left = Node(value=random.choice(OPERATORS))
        node.right = Node(value=random.choice(OPERATORS))
        tree.size += 2
        build_tree(tree, node.left, height+1)
        build_tree(tree, node.right, height+1)
        
    elif 8 <= tree.size <= 12:
        # 50% chance of building a node to the left
        if random.random() < 0.5:
            node.left = Node(value=random.choice(OPERATORS))
            tree.size += 1
            build_tree(tree, node.left, height+1)
        else:
            node.left = Node(value=random.choice(VARIABLES))
            tree.size += 1
            height += 1
        
        # 50% chance of building a node to the right
        if random.random() < 0.5:
            node.right = Node(value=random.choice(OPERATORS))
            tree.size += 1
            build_tree(tree, node.right, height+1)
        else:
            node.right = Node(value=random.choice(VARIABLES))
            tree.size += 1
            height += 1
    
    # Ensures no nodes are empty
    if node.left is None:
        node.left=Node(value=random.choice(VARIABLES))
        tree.size += 1
        height += 1
    if node.right is None:
        node.right=Node(value=random.choice(VARIABLES))
        tree.size += 1
        height += 1
        
def build_graph(fitnesses):
    import matplotlib.pyplot as plt
    plt.plot(fitnesses)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness over Generations")
    plt.show()

# Generate Solutions
def run_genetic_programming():
    print("")
    solutions = []
    fitnesses = []
    for s in range(POPULATION_SIZE):
        new_tree = Tree(Node(random.choice(OPERATORS)))
        build_tree(new_tree, new_tree.root)
        solutions.append(new_tree)
    
    for generation in range(GENERATIONS):
        # Evaluate fitness
        ranked_solutions = [(fitness(s.root), s) for s in solutions]
        ranked_solutions.sort(key=lambda x: x[0], reverse=True)
        
        if ranked_solutions[0][0] >= CUTOFF_FITNESS:
            print(f"Fitness: {ranked_solutions[0][0]}")
            print(f"Solution: {build_string(ranked_solutions[0][1].root)}")
            print(f"Solution found in generation {generation}!")
            build_graph(fitnesses)
            return ranked_solutions[0][1]
        
        # Create new generation
        new_generation = []
        
        # Elitism - keep best 5% unchanged
        elite_count = POPULATION_SIZE // 20
        new_generation.extend([s[1] for s in ranked_solutions[:elite_count]])
        
        # Fill rest of population
        while len(new_generation) < POPULATION_SIZE:
            if random.random() < CROSSOVER_RATE:
                parent1 = tournament_selection(ranked_solutions, TOURNAMENT_SIZE)
                parent2 = tournament_selection(ranked_solutions, TOURNAMENT_SIZE)
                child1, child2 = crossover(parent1, parent2)
                new_generation.extend([child1, child2])
            else:
                parent = tournament_selection(ranked_solutions, TOURNAMENT_SIZE)
                mutated = Tree(mutate(clone(parent.root)))
                new_generation.append(mutated)
        
        # Trim to population size if needed
        solutions = new_generation[:POPULATION_SIZE]
        
        # Adjust tree sizes
        for s in solutions:
            s.size = adjust_tree(s, s.root)
        
        fitnesses.append(ranked_solutions[0][0])
        print(f"Generation {generation}: Best fitness = {ranked_solutions[0][0]}")
        print(f"Best solution: {build_string(ranked_solutions[0][1].root)}")
        print("")

run_genetic_programming()