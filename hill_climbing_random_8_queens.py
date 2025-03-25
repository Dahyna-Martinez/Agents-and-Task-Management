import random
import matplotlib.pyplot as plt
import numpy as np

from hill_climing_random_restart import random_restart_hill_climbing
from search import Problem, Node, argmax_random_tie,hill_climbing


class CustomNQueensProblem(Problem):
    """
    inherits from base problem to solve the 8 queens problem.
    """
    def __init__(self, N):
        self.N = N
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        super().__init__(initial_state)

    def actions(self, state):
        actions = []
        for col in range(self.N):
            for row in range(self.N):
                if state[col] != row:
                    actions.append((col, row))
        return actions

    def result(self, state, action):
        col, row = action
        new_state = list(state)
        new_state[col] = row
        return tuple(new_state)

    def value(self, state):
        """
           Computes the heuristic as the number of non-attacking queen pairs.
           """
        N = len(state)
        total_pairs = (N * (N - 1)) // 2  # Total possible queen pairs
        attacking = 0

        for i in range(N):
            for j in range(i + 1, N):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    attacking += 1

        return total_pairs - attacking  # Maximized by hill climbing

def random_restart_hill_climbing(N, max_restarts=10):

    """
    solves the N-Queens solution on a chessboard.

    Parameters:
        N (int): The number of queens on the board.
        max_restarts (int, optional): Number of restarts. Defaults to 10.

    returns The initial state, solution and the cost for the problem
    """
    #initializing values.
    best_solution = None
    best_value = float('-inf')
    total_search_cost = 0
    num_restarts = 0

    for _ in range(max_restarts):
        #creates the 8 queens problem
        problem = CustomNQueensProblem(N)
        initial_state=problem.initial
        solution, search_cost = hill_climbing(problem)
        num_restarts += 1
        total_search_cost += search_cost
        solution_value = problem.value(solution)
        #found the optimal solution
        if solution_value == (N * (N - 1)) // 2:
            return initial_state,solution, total_search_cost,num_restarts
        #saves the best solution found
        if solution_value > best_value:
            best_solution = solution
            best_value = solution_value

    return initial_state, best_solution, total_search_cost, num_restarts

def plot_nqueens(state, title=""):
    """
    Visualizes an N-Queens solution on a chessboard.

    Parameters:
        state (tuple): The board state, where each index represents a column and
                       the value represents the row where the queen is placed.
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
    plt.show(block=True)


# count number of pairs heuristic: Number of attacking queen pairs
def count_attacking_pairs(state):
    """
    Computes the heuristic cost as the number of attacking queen pairs.

    Parameters:
        state (tuple): The N-Queens state.

    Returns:
        int: The number of attacking queen pairs.
    """
    attacking_pairs = 0
    N = len(state)
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacking_pairs += 1
    return attacking_pairs


# Solve multiple N-Queens instances using Steepest-Ascent Hill Climbing
num_instances = 10
solutions = []
search_costs = []
attacking_pairs = []
solved_count = 0
restarts=[]

for _ in range(num_instances):
    initial_state,solution, search_cost,num_restarts = random_restart_hill_climbing(8)

    # Compute the  heuristic (attacking pairs)
    attacking_pairs_c = count_attacking_pairs(initial_state)

    # Track data for analysis
    search_costs.append(search_cost)
    attacking_pairs.append(attacking_pairs_c)
    restarts.append(num_restarts)

    if count_attacking_pairs(solution) == 0:  # Solution must have 0 attacking pairs
        solved_count += 1

    solutions.append((initial_state, solution, search_cost, num_restarts))

# **Calculate success rate**
success_rate = (solved_count / num_instances) * 100


# **Display each solution’s initial and final state in pop-up windows**
for i, (init_state, sol, cost,restart) in enumerate(solutions):
    print(f"Initial State {i + 1}: {init_state}")
    print(f"Solution {i + 1}: {sol}")
    print(f"Search Cost for Solution {i + 1}: {cost}")
    print(f"Number of restarts used by solution {i+1}: {restart}")

    plot_nqueens(init_state, title=f"Initial State {i + 1} - N-Queens")
    plot_nqueens(sol, title=f"Solution {i + 1} - N-Queens")


# **Create performance analysis plots**
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# **Plot 1: Search Cost vs. Manhattan Distance**
axs[0].scatter(attacking_pairs, search_costs, color='green', alpha=0.7, label="Search Cost")
axs[0].set_xlabel("Number of Attacking Pairs (Initial State)")
axs[0].set_ylabel("Search Cost (Steps Taken)")
axs[0].set_title("Search Cost vs. Number of Attacking Pairs")
axs[0].legend()
axs[0].grid(True)

# **Plot 2: Success Rate (Bar Chart)**
axs[1].bar(["Solved", "Unsolved"], [success_rate, 100 - success_rate], color=['green', 'red'])
axs[1].set_ylabel("Percentage (%)")
axs[1].set_title("Percentage of Solved Problems")
axs[1].set_ylim(0, 100)

plt.tight_layout()
plt.show()


