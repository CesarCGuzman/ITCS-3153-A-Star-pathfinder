# Resources used:
# https://networkx.guide/algorithms/shortest-path/a-star-search/ pseudocode was referenced but honestly it didn't pan out like how I wanted it to
# https://www.youtube.com/watch?v=JtiK0DOeI4A
# https://docs.python.org/3/library/queue.html priority queue docs


# used for the priority queue
# which is used for the open list to get the node with the lowest f value
from queue import PriorityQueue   
import random   # used to generate random start and goal positions

# Node class
class Node:
    
    def __init__(self, r, c, t):
        self.row = r
        self.col = c
        self.type = t
        self.f = 0
        self.g = 0
        self.parent = None

    # the cost function
    def setF(self):
        self.f = self.g + self.h

    # the cost of the path from start to current node
    def setG(self, value):
        self.g = value

    # the heuristic / estimated cost of the path from current node to goal
    def setH(self, value):
        self.h = value

    # the parent node of the node
    def setParent(self, n):
        self.parent = n

    def getF(self):
        return self.f

    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def getParent(self):
        return self.parent

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    # used to compare nodes, python apparently automatically calls this when we use == to compare nodes
    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.row == other.getRow()) and (self.col == other.getCol())
        else:
            return False
    
    # used for the priority queue to compare nodes based on their f value
    def __lt__(self, other):
        if isinstance(other, Node):
            return (self.f < other.getF())
        else:
            return False

    # this is for printing the node in the console
    def __str__(self):
        return "Node: " + str(self.row) + "_" + str(self.col)

def a_star(start, goal, grid):
    # make start and goal nodes
    start_node = Node(start[0], start[1], 1)
    goal_node = Node(goal[0], goal[1], 1)

    # mark start and goal positions with '1' so that it's easier to visualize
    grid[start[0]][start[1]] = '1'
    grid[goal[0]][goal[1]] = '1'

    # open and closed lists
    open_list = PriorityQueue()
    open_list.put((start_node.getF(), start_node)) # put the start node in the open list
    closed_list = []

    # get the neighbors of a node
    def get_neighbors(node):
        neighbors = [] # list of neighbors
        if node.getRow() > 0:
            # Get the node above, if our node is not in the first row
            neighbors.append(Node(node.getRow()-1, node.getCol(), 0))
        if node.getRow() < 14:
            # Get the node below, if our node is not in the last row
            neighbors.append(Node(node.getRow()+1, node.getCol(), 0))
        if node.getCol() > 0:
            # Get the node to the left, if our node is not in the first column
            neighbors.append(Node(node.getRow(), node.getCol()-1, 0))
        if node.getCol() < 14:
            # Get the node to the right, if our node is not in the last column
            neighbors.append(Node(node.getRow(), node.getCol()+1, 0))
        return neighbors

    # calculate the heuristic manhattan distance
    def heuristic(node):
        # returns the absolute value of the difference between the x/y coordinates of the current node and goal node and adds them together
        return abs(node.getRow() - goal_node.getRow()) + abs(node.getCol() - goal_node.getCol())

    while not open_list.empty():
        # get the node with the lowest f value 
        # priority queue sorts the nodes based on their value 
        # smallest first and since 1 is the second element in the list
        # it is not the start node and technically the first element in our list
        current_node = open_list.get()[1]

        if current_node == goal_node:                                        # only runs if we have reached the goal node
            path = []                                                        # list of nodes that make up the path
            while current_node != start_node:                                # while the current node is not the start node
                path.append((current_node.getRow(), current_node.getCol()))  # add the current node to the path
                current_node = current_node.getParent()                      # set the current node to the parent of the current node and do it again until the start node is reached
            path.append((start_node.getRow(), start_node.getCol()))          # after the while is done we should have the start node, so add it to the path
            path.reverse()                                                   # reverse the path so that it starts from the start node
            for step in path:                                                             
                if step != start and step != goal:                           # mark the path with '+' if it's not the start or goal
                    grid[step[0]][step[1]] = '+'
            return grid

        closed_list.append(current_node)                                     # we have visited the current node and will expand it, so add it to the closed list

        for neighbor in get_neighbors(current_node):                         # for each neighbor of the current node
            if neighbor in closed_list or grid[neighbor.getRow()][neighbor.getCol()] == 'X':    # if the neighbor is in the closed list or it's a wall
                continue                                                     # skip it, move on to next neighbor

            currG = current_node.getG() + 1                                  # current g value is the g value of the current node + 1
            
            # if the neighbor is not in the open list or the current g value is less than the g value of the neighbor
            if (neighbor.getF(), neighbor) not in open_list.queue or currG < neighbor.getG():
                neighbor.setG(currG)                                         # set the g value of the neighbor to the current g value
                neighbor.setH(heuristic(neighbor))                           # set the h value of the neighbor to the heuristic
                neighbor.setF()                                              # set the f value of the neighbor
                neighbor.setParent(current_node)                             # set the parent of the neighbor to the current node

                if (neighbor.getF(), neighbor) not in open_list.queue:       # if the neighbor is not in the open list
                    open_list.put((neighbor.getF(), neighbor))               # add it to the open list

    return 

def print_grid(grid):
    grid_str = '' # this variable will be used to print the grid
    for row in grid:
        row_str = ' ' #one row of the grid
        for cell in row:
            # path will be green
            if cell == '+':
                row_str += ' ' + '\033[92m' + str(cell) + '\033[0m' + ' '
            # start and goal will be blue
            elif cell == '1':
                row_str += ' ' + '\033[94m' + str(cell) + '\033[0m' + ' '
            # walls will be red
            elif cell == 'X':
                row_str += ' ' + '\033[91m' + str(cell) + '\033[0m' + ' '
            else:
                row_str += ' ' + str(cell) + ' ' # white
        # add a new line after each row
        grid_str += row_str + '\n'
    print(grid_str)

# Generate random grid, so that the user can select the start and goal pos
grid = [[0 for i in range(15)] for j in range(15)]            # place a 0 in each cell 15x15 cells
num_blocked_cells = random.randint(20, 25)                    # random number of blocked cells we will be using, 25 max, 20 min. Around 10% basically
blocked_cells = []                                            # list of blocked cells, currently empty
for _ in range(num_blocked_cells):                            # for each blocked cell we're supposed to have
    cell = (random.randint(0, 14), random.randint(0, 14))     # get a random cell
    while cell in blocked_cells:                              # while that cell is already in the list of blocked cells
        cell = (random.randint(0, 14), random.randint(0, 14)) # generate a new cell
    blocked_cells.append(cell)                                # if it isnt then we add it to the blocked cells list
for cell in blocked_cells:                                    # for each blocked cell in the list
    grid[cell[0]][cell[1]] = 'X'                              # mark blocked cells with 'X'
print_grid(grid)                                              # print this grid to the user

# ask user for start position
start_row = int(input('Enter starting row (1-15): '))
start_col = int(input('Enter starting column (1-15): '))
start = (start_row - 1, start_col - 1)                        # subtract 1 from each because indexes start at 0

# ask user for goal position
goal_row = int(input('Enter goal row (1-15): '))
goal_col = int(input('Enter goal column (1-15): '))
goal = (goal_row - 1, goal_col - 1)


grid = a_star(start, goal, grid)
if grid:  # if the grid is returned
    print('\n1 = Start and goal \n+ = Path \nX = Blocked cell') # print this
    print_grid(grid) # print the grid
else:
    print('Cannot find a path to the goal')