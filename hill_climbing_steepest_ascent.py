from search import Node
import time

def steepest_ascent_hill_climbing(problem):
    """
    Steepest-Ascent Hill Climbing:
    Always moves to the best available neighbor, stopping when no improvement is possible.
    It does not backtrack so there is a chance of getting stuck.

    Parameters:
        problem (object): Problem for the hill climbing steepest ascent algorithm to solve.

    Returns:
        tuple: (Final state, search cost, execution time)
    """
    # Start time tracking
    start_time = time.time()
    current = Node(problem.initial)
    # Track number of nodes expanded
    search_cost = 0

    while True:
        neighbors = current.expand(problem)
        # Increment the cost by the number of neighbors
        search_cost += len(neighbors)

        if not neighbors:
            break

        best_neighbor = max(neighbors, key=lambda node: problem.value(node.state))

        if problem.value(best_neighbor.state) <= problem.value(current.state):
            # Stop if no improvement
            break

        current = best_neighbor

    # End time tracking
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time

    return current.state, search_cost, execution_time

