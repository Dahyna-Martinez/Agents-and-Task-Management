from search import Node


def steepest_ascent_hill_climbing(problem):
    """
    Steepest-Ascent Hill Climbing:
    Always moves to the best available neighbor, stopping when no improvement is possible.
    """
    current = Node(problem.initial)

    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break  # No neighbors, stop

        # Get the absolute best neighbor (no random tie-breaking)
        best_neighbor = max(neighbors, key=lambda node: problem.value(node.state))

        # Stop if no improvement
        if problem.value(best_neighbor.state) <= problem.value(current.state):
            break

        current = best_neighbor  # Move to the best neighbor

    return current.state  # Return the best found state
