import matplotlib.pyplot as plt
import numpy as np
from hill_climbing_steepest_ascent_eight_puzzle import EightPuzzleProblem, generate_random_puzzle
from hill_climbing_steepest_ascent import steepest_ascent_hill_climbing


def plot_puzzle(state, title=""):
    """
    Plots a given 8-puzzle state in a 3x3 grid.

    Parameters:
        state (tuple): The current board state as a tuple of 9 numbers (0 represents the empty space).
        title (str, optional): Title of the plot.

    Displays:
        A visualization of the 8-puzzle board.
    """
    state_array = np.array(state).reshape(3, 3)  # Convert tuple into a 3x3 NumPy array

    # Display the board as an image
    plt.imshow(state_array, cmap='Greens', interpolation='nearest')

    # Annotate the board with numbers
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(state_array[i][j]), ha='center', va='center', fontsize=20, color='white')

    plt.title(title)
    plt.axis('off')
    # Ensure each plot appears in a separate pop-up window. Kinda does what I want it to?
    plt.show(block=True)


# Solve multiple instances of the 8-Puzzle using Steepest-Ascent Hill Climbing

# Number of puzzle instances to generate and solve
num_instances = 10
solutions = []

for _ in range(num_instances):
    # Generate a random solvable puzzle state
    initial_state = generate_random_puzzle()
    # Create an 8-Puzzle problem instance
    problem = EightPuzzleProblem(initial_state)
    # Solve using hill climbing
    solution = steepest_ascent_hill_climbing(problem)
    solutions.append((initial_state, solution))

# Print and plot each puzzle instance
for i, (init, sol) in enumerate(solutions):
    print(f"Puzzle {i + 1}: Initial {init} -> Solved {sol}")

    # Display the initial puzzle state
    print(f"Displaying Puzzle {i + 1} - Initial State:")
    plot_puzzle(init, title=f"Puzzle {i + 1} - Initial State")

    # Display the solved puzzle state
    print(f"Displaying Puzzle {i + 1} - Solved State:")
    plot_puzzle(sol, title=f"Puzzle {i + 1} - Solved State")
