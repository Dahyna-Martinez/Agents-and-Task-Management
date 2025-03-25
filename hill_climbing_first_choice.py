import random
from search import Node

def hill_climbing_first_choice(problem, attempt_limit=100000):
    """
    Hill Climbing First Choice:
    - Moves to a randomly selected neighbor node only if it's better than the current state.
    - If no better neighbor is found within the attempt limit, the search stops.

    Parameters:
        problem (Problem): The problem to solve.
        attempt_limit (int): Max number of attempts to find a better neighbor.

    Returns:
        tuple: (Final state, search cost) or (None, None) if not solved.
    """

    current = Node(problem.initial)
    #Tracks the number of nodes that are expanded.
    search_cost = 0

    # Verifies if the initial state is already the goal state.
    if problem.goal_test(current.state):
        return current, search_cost

    while True:
        attempts = 0
        improved = False

        # While the attempt limit has not been reached.
        while attempts < attempt_limit:
            neighbors = current.expand(problem)
            search_cost += 1

            # If there are no neighbors in the list the search terminates.
            if not neighbors:
                return current, search_cost

            # Pick a random neighbor from the node list.
            random_neighbor = random.choice(neighbors)

            # If the new state is better than the current state, move to that neighbor.
            if problem.value(random_neighbor.state) < problem.value(current.state):
                current = random_neighbor
                improved = True
                # Restarts the attempt count with the new state.
                break

            attempts += 1

        # If no improvement was found then terminate the search.
        if not improved:
            break

    return current, search_cost
