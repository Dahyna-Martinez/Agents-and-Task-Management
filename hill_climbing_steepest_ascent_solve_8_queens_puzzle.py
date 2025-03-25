import matplotlib.pyplot as plt
import numpy as np
from search import Problem
#from hill_climbing_first_choice import hill_climbing_first_choice
from hill_climbing_steepest_ascent import steepest_ascent_hill_climbing
import random


class CustomNQueensProblem(Problem):
    """
    Modified N-Queens problem for use with hill climbing.
    The goal is to place N queens on an N×N chessboard such that no two queens attack each other.

    Attributes:
        N (int): The number of queens (and board size).
        initial (tuple): The initial state representing queen positions in each column.

    Methods:
        actions(state): Returns all possible moves by changing a queen's row in any column.
        result(state, action): Returns a new state with the given move applied.
        value(state): Computes the heuristic value based on the number of attacking queen pairs.
    """

    def __init__(self, N):
        """
        Initializes an N-Queens problem with a randomly generated initial state.

        Parameters:
            N (int): The number of queens and the size of the board.
        """
        self.N = N
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        super().__init__(initial_state)

    def actions(self, state):
        """
        Generates all possible moves by changing a queen's row in any column.

        Parameters:
            state (tuple): The current board state.

        Returns:
            list: A list of possible moves as tuples (col, row).
        """
        actions = []
        for col in range(self.N):
            for row in range(self.N):
                if state[col] != row:
                    actions.append((col, row))
        return actions

    def result(self, state, action):
        """
        Generates a new state by moving a queen to a different row in a specific column.

        Parameters:
            state (tuple): The current board state.
            action (tuple): A tuple (col, row) specifying which queen to move and where.

        Returns:
            tuple: The new board state after applying the move.
        """
        col, row = action
        new_state = list(state)
        new_state[col] = row
        return tuple(new_state)

    def value(self, state):
        """
        Computes the heuristic value of a state based on the number of attacking queen pairs.

        Parameters:
            state (tuple): The current board state.

        Returns:
            int: The number of attacking queen pairs.
        """
        attacking_pairs = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    attacking_pairs += 1
        return -attacking_pairs


def plot_nqueens(state, title=""):
    """
    Visualizes an N-Queens solution on a chessboard.

    Parameters:
        state (tuple): The board state.
        title (str, optional): The title for the plot.
    """
    N = len(state)
    board = np.zeros((N, N))
    for col, row in enumerate(state):
        board[row, col] = 1

    plt.imshow(board, cmap='Greens', interpolation='nearest')
    for col in range(N):
        row = state[col]
        plt.text(col, row, 'Q', ha='center', va='center', fontsize=20, color='White')

    plt.grid(which='both', color='black', linestyle='--', linewidth=2)
    plt.title(title)
    plt.axis('off')
    plt.grid(True)
    plt.show(block=True)


def calculate_min_moves_to_solution(state):
    """
    Estimates the minimum number of moves needed to transform an initial state into a valid solution.

    Parameters:
        state (tuple): The initial state of the board.

    Returns:
        int: The minimum number of queen moves required.
    """
    N = len(state)
    #Count how many queens are in each row.
    row_conflicts = [0] * N
    for row in state:
        row_conflicts[row] += 1

    # The minimum number of moves is at least the number of excess queens in conflicting rows.
    excess_queens = sum(c - 1 for c in row_conflicts if c > 1)

    return excess_queens  # A rough lower bound on moves needed to fix the state


# Solve multiple N-Queens instances using First Choice Hill Climbing.
num_instances = 10
solutions = []
search_costs = []
optimal_solution_costs = []
solved_count = 0

for i in range(num_instances):
    problem = CustomNQueensProblem(8)
    initial_state = problem.initial
    solution_node, search_cost,execution_time = steepest_ascent_hill_climbing(problem)

    # Extract the solution state if it's a Node object.
    solution = solution_node.state if hasattr(solution_node, 'state') else solution_node

    # Compute the optimal solution cost (attacking pairs) for the initial state.
    optimal_solution_cost = calculate_min_moves_to_solution(initial_state)

    # Check if the solution is successful
    solved = problem.value(solution) == 0
    success_percentage = (1 if solved else 0) * 100  # 100% if solved, else 0%

    # Track data for analysis
    search_costs.append(search_cost)
    optimal_solution_costs.append(optimal_solution_cost)

    if solved:
        solved_count += 1

    solutions.append((initial_state, solution, search_cost))

    # Print success for each instance
    print(f"Problem {i + 1}: {'Solved' if solved else 'Unsolved'} ({success_percentage}%)")
    print(f"Initial State: {initial_state}")
    print(f"Solution: {solution}")
    print(f"Search Cost: {search_cost}")
    print(f"Optimal Solution Cost: {optimal_solution_cost}\n")

    plot_nqueens(initial_state, title=f"Initial State {i + 1} - N-Queens")
    plot_nqueens(solution, title=f"Solution {i + 1} - N-Queens")

# Calculate overall success rate
success_rate = (solved_count / num_instances) * 100
print(f"Overall Success Rate: {success_rate:.2f}%")

# Create performance analysis plots.
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Search Cost vs. Attacking Pairs Costs
axs[0].scatter(optimal_solution_costs, search_costs, color='green', alpha=0.7, label="Search Cost")
axs[0].set_xlabel("Number of Attacking Pairs (Initial State)")
axs[0].set_ylabel("Search Cost (Steps Taken)")
axs[0].set_title("Search Cost vs. Number of Attacking Pairs")
axs[0].legend()
axs[0].grid(True)

# Plot 2: Success Rate (Bar Chart)
axs[1].bar(["Solved", "Unsolved"], [success_rate, 100 - success_rate], color=['green', 'red'])
axs[1].set_ylabel("Percentage (%)")
axs[1].set_title("Percentage of Solved Problems")
axs[1].set_ylim(0, 100)

plt.tight_layout()
plt.show()
