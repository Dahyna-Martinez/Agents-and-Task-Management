import random
import matplotlib.pyplot as plt
from hill_climbing_first_choice import hill_climbing_first_choice
from hill_climbing_first_choice_eight_puzzle import FirstChoiceHillClimbingEightProblem


def generate_random_eight_puzzle_state():
    """Generates a random 8-puzzle state."""
    state = list(range(9))
    random.shuffle(state)
    return tuple(state)


def manhattan_distance(state, goal_state):
    """
       Calculates the Manhattan Heuristic values. It evaluates the state based on the sum of Manhattan
       distances from their positions in the goal states.
        A value closer to 0 indicates a better state.

    Parameters:
        goal_state (tuple): The goal state of the puzzle as a tuple of integers.

    Returns:
        int: The sum of the Manhattan distances excluding the blank tile.
    """

    distance = 0
    # Iterates through all tiles in the grid.
    for i in range(9):
        # Ignores the empty tile (0).
        if state[i] != 0:
            target_pos = goal_state.index(state[i])
            current_row, current_col = divmod(i, 3)
            target_row, target_col = divmod(target_pos, 3)
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


def plot_eight_puzzle_state(initial_state, solved_state, puzzle_num):
    """
     Uses matplotlib to plot the initial and the end states of each puzzle.

     Parameters:
         initial_state (tuple): A tuple of integers that represent the current puzzle state, where the
         blank tile is 0.

         solved_state (tuple): A tuple of integers representing the state
         up to where the program could solve the puzzle.

         puzzle_num (int): An identifier that indicated which puzzle problem is currently being solved.

     """
    # Creates a 1 by 2 grid. One column for the initial state and the other for the goal state.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    def plot_state(ax, state, title):
        # Reshapes the list into a 3 by 3 grid.
        ax.imshow([[state[i * 3 + j] for j in range(3)] for i in range(3)], cmap='Greens', interpolation='nearest')
        ax.set_title(title)
        # Adds numbers to the tiles.
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(state[i * 3 + j]), ha='center', va='center', fontsize=16, color='black', fontweight='bold')
        ax.axis('off')

    # Plots the initial State and Goal State.
    plot_state(axes[0], initial_state, f'Puzzle {puzzle_num} - Initial State')
    plot_state(axes[1], solved_state, f'Puzzle {puzzle_num} - Solved State')

    plt.tight_layout()
    plt.show()


# Generates 10 problems to solve with first choice hill climbing.
initial_states = [generate_random_eight_puzzle_state() for _ in range(10)]
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

search_costs = []
solved_percentage = []
optimal_costs = []

for puzzle_num, initial_state in enumerate(initial_states, start=1):
    # Solves each 8-puzzle problem.
    problem = FirstChoiceHillClimbingEightProblem(initial_state)

    result = hill_climbing_first_choice(problem)

    if result[0] is None:
        print(f"Puzzle {puzzle_num} - Hill climbing failed! Skipping this puzzle.")
        # Skip to the next puzzle if the problem could not be solved.
        continue

    final_state, search_count = result

    optimal_cost = manhattan_distance(initial_state, goal_state)
    optimal_costs.append(optimal_cost)
    search_costs.append(search_count)

    solved = 1 if final_state.state == goal_state else 0
    solved_percentage.append(solved)

    # Prints the results in the terminal.
    print(f"\nPuzzle {puzzle_num}")
    print(f"Initial State: {initial_state}")
    print(f"Final State: {final_state.state}")
    print(f"Search Count: {search_count}")
    print(f"Optimal Cost (Manhattan Distance): {optimal_cost}")
    print(f"Percentage Completed: {solved * 100}%")

    plot_eight_puzzle_state(initial_state, final_state.state, puzzle_num)

# Calculate the percentage of solved problems.
solved_count = sum(solved_percentage)
total_problems = len(initial_states)
solved_percentage_total = (solved_count / total_problems) * 100

# Print out the percentage of solved problems.
print(f"\nPercentage of Solved Problems: {solved_percentage_total:.2f}%")

# Ensure lists are the same size before plotting.
if len(optimal_costs) == len(search_costs) == len(solved_percentage):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Use the overall solved percentage for plotting
    ax.scatter(optimal_costs, search_costs, color='blue', label='Search Cost')
    ax.scatter(optimal_costs, [solved_percentage_total] * len(optimal_costs), color='red', label='Solved Percentage')

    ax.set_xlabel("Optimal Solution Cost (Manhattan Distance)")
    ax.set_ylabel("Search Cost / Solved Percentage")
    ax.set_title("Search Cost and Solved Percentage vs Optimal Solution Cost")
    ax.legend()

    plt.show()
else:
    print("Warning: List size mismatch! Scatter plot skipped.")
