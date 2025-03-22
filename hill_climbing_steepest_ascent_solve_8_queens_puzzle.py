import matplotlib.pyplot as plt
import numpy as np
from search import Problem
from hill_climbing_steepest_ascent import steepest_ascent_hill_climbing
import random


class CustomNQueensProblem(Problem):
    """Modified N-Queens problem that includes a value() function for hill climbing."""

    def __init__(self, N):
        self.N = N
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        super().__init__(initial_state)

    def actions(self, state):
        """Returns all possible moves (changing a queen's row in any column)."""
        actions = []
        for col in range(self.N):
            for row in range(self.N):
                if state[col] != row:
                    actions.append((col, row))
        return actions

    def result(self, state, action):
        """Returns a new state with the given move applied."""
        col, row = action
        new_state = list(state)
        new_state[col] = row
        return tuple(new_state)

    def value(self, state):
        """Counts the number of non-attacking pairs of queens (to maximize)."""
        non_attacking_pairs = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if state[i] != state[j] and abs(state[i] - state[j]) != abs(i - j):
                    non_attacking_pairs += 1
        return non_attacking_pairs


def plot_nqueens(state, title=""):
    """
    Function to plot the N-Queens solution in a grid.
    """
    N = len(state)
    board = np.zeros((N, N))  # Create an N x N board, initially empty (0's)

    # Place queens on the board (1 for queen)
    for col, row in enumerate(state):
        board[row, col] = 1

    # Plot the board with grid lines
    plt.imshow(board, cmap='Greens', interpolation='nearest')

    # Label queens on the board
    for col in range(N):
        row = state[col]
        plt.text(col, row, 'Q', ha='center', va='center', fontsize=20, color='White')

    # Add grid lines
    plt.grid(which='both', color='black', linestyle='--', linewidth=2)  # Make grid squares visible

    plt.title(title)
    plt.axis('off')  # Hide axes
    plt.show(block=True)  # Ensure it's a pop-up


# Solve multiple N-Queens instances
num_instances = 10
solutions = []

for _ in range(num_instances):
    problem = CustomNQueensProblem(8)  # Use custom problem class
    solution = steepest_ascent_hill_climbing(problem)
    solutions.append(solution)

# Print results and plot for each solution
for i, sol in enumerate(solutions):
    print(f"Solution {i + 1}: {sol}")

    # Plot the solution
    print(f"Displaying Solution {i + 1}:")
    plot_nqueens(sol, title=f"Solution {i + 1} - N-Queens")
