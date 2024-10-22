import random
# Hyperparameters
POPULATION_SIZE = 1000      # Number of solutions in the population
GENERATIONS = 500        # Number of generations to run

MUTATION_RATE = 0.3         # 20% chance of initiating mutation
MUTATION_CHANCE = 0.5       # 50% chance of mutating a node during mutation
CROSSOVER_RATE = 0.3        # 30% crossover rate
REPLICATION_RATE = 0.2     # 20% replication rate

OPERATORS = ['+', '-', '*', '/']
VARIABLES = ['x', 'y', 'z']
CUTOFF_FITNESS = 1000     # The fitness at which we consider the solution found
MAX_HEIGHT = 8              # The maximum depth of the tree (A higher number might require increasing Python's limit)

goal = 570.7149963378906 # Next minute's open price
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

    if ans <= 1:
        return CUTOFF_FITNESS
    else:
        return abs(1 / ans)

# Method to perform crossover between two trees
def crossover(parent1, parent2):
    # Clone the parents
    tree1 = Tree(clone(parent1.root))
    tree2 = Tree(clone(parent2.root))
    
    # Select random nodes from each tree
    node1 = get_random_node(tree1.root)
    node2 = get_random_node(tree2.root)
    
    # Swap subtrees
    temp = node1.left
    node1.left = node2.left
    node2.left = temp
    
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
def mutate(node):
    if print_method_names: print("Mutate")
    # Base Case, don't mutate leaf or null nodes
    if node == None or node.value in VARIABLES:
        return node
    
    # 80% chance of mutating a node
    if random.random() < MUTATION_CHANCE:
        node.value = random.choice(OPERATORS)
    
    node.left = mutate(node.left)
    node.right = mutate(node.right)      
    
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
        
# Generate Solutions
solutions = []
for s in range(POPULATION_SIZE):
    new_tree = Tree(Node(random.choice(OPERATORS)))
    build_tree(new_tree, new_tree.root)
    solutions.append(new_tree)
    
# Main loop
for i in range(GENERATIONS):
    if print_solution_sizes: print("Generation", i, "Population Size:", len(solutions))
    rankedsolutions = []
    for s in solutions:
        rankedsolutions.append( (fitness(s.root), s) )
    rankedsolutions.sort(key=lambda x: x[0], reverse=True)
    
    print(f"Gen {i} best fitness: {build_string(rankedsolutions[0][1].root)}")
    
    # If the fitness is over a certain amount, we consider it fit enough
    if rankedsolutions[0][0] >= CUTOFF_FITNESS:
        print(f"=== Gen {i} solutions ===")
        print(rankedsolutions[0], build_string(rankedsolutions[0][1].root))
        print("Solution found!")
        break
    
    # Keep 10% of the best solutions
    bestsolutions = rankedsolutions[:POPULATION_SIZE // 10]
    
    # Build new population
    newgen = []
    for i in range(POPULATION_SIZE):
        if random.random() < REPLICATION_RATE:
            newgen.append(random.choice(bestsolutions)[1])
        elif random.random() < CROSSOVER_RATE:
            parent1 = random.choice(bestsolutions)[1]
            parent2 = random.choice(bestsolutions)[1]

            # Crossover
            child1, child2 = crossover(parent1, parent2)
            newgen.append(child1)
            newgen.append(child2)
            i += 1
        else:
            new_pop = Tree(root = mutate( random.choice(bestsolutions)[1].root))
            newgen.append(new_pop)
    
    solutions = newgen
    
    # Adjust the size of each solution
    for s in solutions:
        # print("\n")
        s.size = adjust_tree(s, s.root)

