import matplotlib.pyplot as plt
import numpy as np
from search import Problem
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
        value(state): Computes the heuristic value based on the number of non-attacking queen pairs.
    """

    def __init__(self, N):
        """
        Initializes an N-Queens problem with a randomly generated initial state.

        Parameters:
            N (int): The number of queens and the size of the board.
        """
        self.N = N
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))  # Randomly place queens in each column
        super().__init__(initial_state)

    def actions(self, state):
        """
        Generates all possible moves by changing a queen's row in any column.

        Parameters:
            state (tuple): The current board state, where each index represents a column and
                           the value represents the row where the queen is placed.

        Returns:
            list: A list of possible moves as tuples (col, row), where 'col' is the column index
                  and 'row' is the new row position.
        """
        actions = []
        for col in range(self.N):
            for row in range(self.N):
                if state[col] != row:  # Ensure we are making a change
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
        Computes the heuristic value of a state based on the number of non-attacking queen pairs.
        A higher value indicates a better state.

        Parameters:
            state (tuple): The current board state.

        Returns:
            int: The number of non-attacking queen pairs.
        """
        non_attacking_pairs = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if state[i] != state[j] and abs(state[i] - state[j]) != abs(i - j):
                    # Check if queens are not on the same row or diagonal
                    non_attacking_pairs += 1
        return non_attacking_pairs


def plot_nqueens(state, title=""):
    """
    Visualizes an N-Queens solution on a chessboard.

    Parameters:
        state (tuple): The board state, where each index represents a column and
                       the value represents the row where the queen is placed.
        title (str, optional): The title for the plot.
    """
    N = len(state)
    board = np.zeros((N, N))  # Create an N×N empty board

    # Place queens on the board
    for col, row in enumerate(state):
        board[row, col] = 1

    # Plot the board
    plt.imshow(board, cmap='Greens', interpolation='nearest')

    # Label queens on the board
    for col in range(N):
        row = state[col]
        plt.text(col, row, 'Q', ha='center', va='center', fontsize=20, color='White')

    # Add grid lines for better visualization
    plt.grid(which='both', color='black', linestyle='--', linewidth=2)

    plt.title(title)
    plt.axis('off')  # Hide axes
    plt.show(block=True)  # Ensure it opens as a pop-up window


# Solve multiple N-Queens instances using Steepest-Ascent Hill Climbing
num_instances = 10  # Number of problem instances to solve
solutions = []

for _ in range(num_instances):
    problem = CustomNQueensProblem(8)  # Create an 8-Queens problem instance
    solution = steepest_ascent_hill_climbing(problem)  # Solve using hill climbing
    solutions.append(solution)

# Print and plot each solution
for i, sol in enumerate(solutions):
    print(f"Solution {i + 1}: {sol}")

    # Display the solution
    print(f"Displaying Solution {i + 1}:")
    plot_nqueens(sol, title=f"Solution {i + 1} - N-Queens")
