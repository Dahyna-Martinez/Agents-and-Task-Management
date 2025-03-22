import matplotlib.pyplot as plt
import numpy as np
from hill_climbing_steepest_ascent_eight_puzzle import EightPuzzleProblem, generate_random_puzzle
from hill_climbing_steepest_ascent import steepest_ascent_hill_climbing


def plot_puzzle(state, title=""):
    """
    Function to plot the 8-puzzle state in a 3x3 grid.
    """
    state_array = np.array(state).reshape(3, 3)
    plt.imshow(state_array, cmap='Greens', interpolation='nearest')
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(state_array[i][j]), ha='center', va='center', fontsize=20, color='white')
    plt.title(title)
    plt.axis('off')
    plt.show(block=True)  # Ensures each plot appears in a pop-up window


# Generate and solve multiple instances
num_instances = 10  # You can increase this
solutions = []

for _ in range(num_instances):
    initial_state = generate_random_puzzle()
    problem = EightPuzzleProblem(initial_state)
    solution = steepest_ascent_hill_climbing(problem)
    solutions.append((initial_state, solution))

# Print results and plot for each puzzle
for i, (init, sol) in enumerate(solutions):
    print(f"Puzzle {i + 1}: Initial {init} -> Solved {sol}")

    # Plot initial state
    print(f"Displaying Puzzle {i + 1} - Initial State:")
    plot_puzzle(init, title=f"Puzzle {i + 1} - Initial State")

    # Plot solved state
    print(f"Displaying Puzzle {i + 1} - Solved State:")
    plot_puzzle(sol, title=f"Puzzle {i + 1} - Solved State")
