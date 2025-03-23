import matplotlib.pyplot as plt
import numpy as np
from hill_climbing_steepest_ascent_eight_puzzle import EightPuzzleProblem, generate_random_puzzle
from hill_climbing_steepest_ascent import steepest_ascent_hill_climbing


# Function to calculate the Manhattan distance (optimal solution cost)
def manhattan_distance(state, goal_state):
    """
    Computes the Manhattan distance of the given 8-puzzle state from the goal state.

    Parameters:
        state (tuple): The current board state as a tuple of 9 numbers (0 represents the empty space).
        goal_state (tuple): The target goal state to compare against.

    Returns:
        int: The Manhattan distance (sum of tile moves required to reach the goal).
    """
    distance = 0
    for i in range(9):
        if state[i] != 0:
            target_pos = goal_state.index(state[i])
            current_row, current_col = divmod(i, 3)
            target_row, target_col = divmod(target_pos, 3)
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


# Function to plot a 3×3 puzzle state
def plot_puzzle(state, title=""):
    """
    Plots a given 8-puzzle state in a 3x3 grid.

    Parameters:
        state (tuple): The current board state as a tuple of 9 numbers (0 represents the empty space).
        title (str, optional): Title of the plot.

    Displays:
        A visualization of the 8-puzzle board.
    """
    # Convert tuple into a 3x3 NumPy array
    state_array = np.array(state).reshape(3, 3)

    # Display the board as an image
    plt.imshow(state_array, cmap='Greens', interpolation='nearest')

    # Annotate the board with numbers
    for i in range(3):
        for j in range(3):
            text_color = 'white' if state_array[i, j] != 0 else 'black'
            plt.text(j, i, str(state_array[i, j]), ha='center', va='center', fontsize=20, color=text_color)

    plt.title(title)
    plt.axis('off')
    plt.show(block=True)


# Number of random puzzles to generate and solve
num_instances = 10
# Standard 8-puzzle goal state
goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

# Lists to store results
search_costs = []  # Stores the number of steps taken by hill climbing
manhattan_costs = []  # Stores the optimal solution cost estimated by Manhattan distance
solved_count = 0  # Counter for the number of successfully solved puzzles
solutions = []  # Stores puzzle instances for visualization

# Solve multiple instances of the 8-Puzzle using Steepest-Ascent Hill Climbing
for _ in range(num_instances):
    # Generate a random solvable puzzle state
    initial_state = generate_random_puzzle()
    problem = EightPuzzleProblem(initial_state)

    # Solve the puzzle using hill climbing
    solution, search_cost, execution_time = steepest_ascent_hill_climbing(problem)

    # Compute the Manhattan distance (heuristic estimate of the optimal cost)
    manhattan_cost = manhattan_distance(initial_state, goal_state)

    # Store results for analysis
    search_costs.append(search_cost)
    manhattan_costs.append(manhattan_cost)

    # Count successfully solved problems
    if solution == goal_state:
        solved_count += 1

    # Store puzzle instance for later visualization
    solutions.append((initial_state, solution, search_cost, execution_time))


# **Display each puzzle’s initial and solved state in pop-up windows**
for i, (init, sol, cost, time) in enumerate(solutions):
    print(f"Puzzle {i + 1}: Initial {init} -> Solved {sol}")
    print(f"Search Cost for Puzzle {i + 1}: {cost}")
    print(f"Execution Time for Puzzle {i + 1}: {time:.4f} seconds")

    # Display the initial puzzle state
    plot_puzzle(init, title=f"Puzzle {i + 1} - Initial State")

    # Display the solved puzzle state
    plot_puzzle(sol, title=f"Puzzle {i + 1} - Solved State")


# **Create a single figure with two subplots for analysis**
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
success_rate = (solved_count / num_instances) * 100



# **Plot 1: Search Cost vs. Manhattan Distance**
# Blue for search cost
axs[0].scatter(manhattan_costs, search_costs, color='blue', alpha=0.7, label="Search Cost")
# Green for heuristic
axs[0].scatter(manhattan_costs, manhattan_costs, color='green', alpha=0.7, label="Manhattan Distance")
axs[0].set_xlabel("Manhattan Distance (Optimal Cost)")
axs[0].set_ylabel("Search Cost (Steps Taken)")
axs[0].set_title("Search Cost vs. Manhattan Distance")
axs[0].legend()
axs[0].grid(True)

# **Plot 2: Success Rate (Bar Chart)**
axs[1].bar(["Solved", "Unsolved"], [success_rate, 100 - success_rate], color=['green', 'red'])
axs[1].set_ylabel("Percentage (%)")
axs[1].set_title("Percentage of Solved Problems")
axs[1].set_ylim(0, 100)

# Show both plots in a single figure
plt.tight_layout()
plt.show()
