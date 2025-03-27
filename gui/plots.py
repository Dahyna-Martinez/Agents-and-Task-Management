import matplotlib.pyplot as plt

"""
8puzzle: 
optimal_solution_costs = [8,8,5,11,20,8,9,18,9,18]  # optimal costs
search_costs = [99,99,100,100,97,100,99,95,99,95]  # search costs (steps taken)
success_rate = 0  # success rate in percentage
"""

"""
8queens:
optimal_solution_costs = [8,8,8,8,8,8,8,8,8,8]  # optimal costs
search_costs = [11,8,8,10,8,9,10,5,8,10,]  # search costs (steps taken)
success_rate = 20  # success rate in percentage
"""

"""
8queensV2: 
optimal_solution_costs = [3,5,4,4,6,6,3,4,5,3]  # optimal costs
search_costs = [101,101,101,101,101,101,101,101,101,101]  # search costs (steps taken)
success_rate = 0  # success rate in percentage
"""
# Hardcoded data 
optimal_solution_costs = [3,5,4,4,6,6,3,4,5,3]  # optimal costs
search_costs = [101,101,101,101,101,101,101,101,101,101]  # search costs (steps taken)
success_rate = 0  # success rate in percentage

# Create performance analysis plots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Search Cost vs. Optimal Cost
axs[0].scatter(optimal_solution_costs, search_costs, color='green', alpha=0.7, label="Search Cost")
axs[0].set_xlabel("Optimal Cost")
axs[0].set_ylabel("Search Cost (Steps Taken)")
axs[0].set_title("Search Cost vs. Optimal Cost")
axs[0].legend()
axs[0].grid(True)

# Plot 2: Success Rate (Bar Chart)
axs[1].bar(["Solved", "Unsolved"], [success_rate, 100 - success_rate], color=['green', 'red'])
axs[1].set_ylabel("Percentage (%)")
axs[1].set_title("Percentage of Solved Problems")
axs[1].set_ylim(0, 100)

plt.tight_layout()
plt.show()
