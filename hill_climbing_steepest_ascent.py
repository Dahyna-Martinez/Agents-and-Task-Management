from search import Node


def steepest_ascent_hill_climbing(problem):
    """
    Steepest-Ascent Hill Climbing:
    Always moves to the best available neighbor, stopping when no improvement is possible.
    It does not backtrack so there is a chance of getting stuck.

    Parameters:
                    problem (object): Problem for the hill climbing steepest ascent algorithm
                    to solve.
    Returns:
        List of best found state. Not necessarily a solution.

    """
    current = Node(problem.initial)

    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break

        # Get the absolute best neighbor
        best_neighbor = max(neighbors, key=lambda node: problem.value(node.state))

        # Stop if no improvement to avoid infinite looping
        if problem.value(best_neighbor.state) <= problem.value(current.state):
            break
        # Move to the best neighbor
        current = best_neighbor

        # Return the best found state
    return current.state
