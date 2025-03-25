import matplotlib.pyplot as plt
import numpy as np

from hill_climing_random_restart import random_restart_hill_climbing


def manhattan_distance(state, ):
    goal_positions = {val: (i // 3, i % 3) for i, val in enumerate((1, 2, 3, 4, 5, 6, 7, 8,0))}
    distance = sum(abs(r - goal_positions[val][0]) + abs(c - goal_positions[val][1])
                   for i, val in enumerate(state) if val != 0
                   for r, c in [divmod(i, 3)])
    return distance

def plot_puzzle(state, title=""):
    state_array = np.array(state).reshape(3, 3)
    plt.imshow(state_array, cmap='Greens', interpolation='nearest')

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
goal_state = ( 1, 2, 3, 4, 5, 6, 7, 8,0)

# Lists to store results
search_costs = []
manhattan_costs = []
restart_used_cost=[]
solved_count = 0
solutions = []

# Solve multiple instances of the 8-Puzzle using Steepest-Ascent Hill Climbing
for _ in range(num_instances):
    # Generate a random solvable puzzle state
    initial_state,solution, search_cost,restart_used= random_restart_hill_climbing()

    # Compute the Manhattan distance (heuristic estimate of the optimal cost)
    manhattan_cost = manhattan_distance(initial_state)

    # Store results for analysis
    search_costs.append(search_cost)
    manhattan_costs.append(manhattan_cost)
    restart_used_cost.append(restart_used)
    # Count successfully solved problems
    if solution == goal_state:
        solved_count += 1
    # Store puzzle instance for later visualization
    solutions.append((initial_state, solution, search_cost, restart_used))


# **Display each puzzle’s initial and solved state in pop-up windows**
for i, (init, sol, cost,restart_used) in enumerate(solutions):
    print(f"Puzzle {i + 1}: Initial {init} -> Solved {sol}")
    print(f"Search Cost for Puzzle {i + 1}: {cost}")
    print(f"Restart Used Cost for Puzzle {i + 1}: {restart_used}")

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
