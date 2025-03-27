#8-queens
import os
import sys
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import Node
from search import Problem, astar_search

class NQueensProblemV2(Problem):
    """A* search version of the N-Queens problem where queens can move within their columns."""
    
    def __init__(self, N, initial_state):
        self.N = N
        self.initial = initial_state
        super().__init__(self.initial)

    def actions(self, state):
        """Generate valid moves by changing a queen's row in a column."""
        actions = []
        for col in range(self.N):
            for row in range(self.N):
                if state[col] != row:  # Move only if the row is different
                    actions.append((col, row))
        return actions

    def result(self, state, action):
        """Apply an action by changing a queen’s row position in a column."""
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)

    def goal_test(self, state):
        """Check if the state is a valid solution (no attacking queens)."""
        return self.h(state) == 0  # No conflicts means solution found

    def h(self, node_or_state):
        """Heuristic function: Count number of conflicting queen pairs."""
        # Ensure we always work with the state (whether node or tuple)
        state = node_or_state.state if isinstance(node_or_state, Node) else node_or_state  

        conflicts = 0
        for col1 in range(self.N):
            for col2 in range(col1 + 1, self.N):
                if self.conflict(state[col1], col1, state[col2], col2):
                    conflicts += 1
        return conflicts

    def conflict(self, row1, col1, row2, col2):
        """Check if two queens are in conflict."""
        return row1 == row2 or abs(row1 - row2) == abs(col1 - col2)

# List of initial states
nqueens_states = [
    (0,4,5,1,7,2,6,3),  
    (1,2,3,7,4,5,6,0),
    (0,4,2,6,5,3,1,7),
    (7,3,6,2,1,4,0,5),
    (4,2,1,0,3,5,6,7),
    (2,1,4,3,5,6,7,0),
    (0,7,5,4,2,1,6,3),
    (5,3,4,0,2,6,7,1),
    (1,3,5,2,7,4,0,6),
    (5,3,1,7,4,2,6,0)
]

# Solve each N-Queens instance using A* search and print the optimal cost
for i, state in enumerate(nqueens_states, start=1):
    problem = NQueensProblemV2(8, state)  # Initialize with 8 queens
    solution_node = astar_search(problem)  # Perform A* search
    
    if solution_node is None:
        print(f"N-Queens Board {i} - No Solution Found")
    else:
        solution_path = solution_node.solution()  # Sequence of moves
        optimal_cost = len(solution_path)  # Number of moves to reach the goal
        print(f"N-Queens Board {i} - Optimal Solution Cost: {optimal_cost}")

#8-puzzle
""""
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import astar_search, EightPuzzle

# List of puzzle states to evaluate
puzzle_states = [
    (2, 3, 6, 1, 5, 8, 4, 7, 0),
    (1, 5, 2, 4, 3, 6, 0, 7, 8),
    (2, 0, 3, 1, 4, 6, 7, 5, 8),
    (1, 3, 6, 0, 7, 2, 5, 4, 8),
    (4, 5, 0, 7, 6, 1, 3, 2, 8),
    (2, 5, 3, 1, 7, 6, 0, 4, 8),
    (4, 1, 2, 5, 3, 6, 7, 0, 8),
    (3, 4, 2, 1, 7, 6, 5, 8, 0),
    (5, 1, 3, 4, 2, 6, 7, 0, 8),
    (0, 8, 3, 2, 5, 6, 7, 1, 4)
]

# Solve each puzzle using A* search and print the optimal cost
for i, state in enumerate(puzzle_states, start=1):
    puzzle = EightPuzzle(state)
    solution = astar_search(puzzle)
    optimal_cost = len(solution.solution())  # Number of moves in the optimal solution
    print(f"Puzzle {i} - Optimal Solution Cost: {optimal_cost}")"
    """
