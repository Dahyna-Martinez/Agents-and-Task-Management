import random
from search import Problem,hill_climbing,EightPuzzle

def generate_random_puzzle():
    """
    Generates a solvable random 8-Puzzle instance by shuffling the tiles.
    Ensures the puzzle is solvable.
    """
    for _ in range(100):
        puzzle = list(range(9))
        random.shuffle(puzzle)
        if EightPuzzle(puzzle).check_solvability(puzzle):
            return tuple(puzzle)


def random_restart_hill_climbing(max_restarts=10):
    """
    Applies hill climbing with random restarts to solve the 8-puzzle.
    Restarts when stuck in a local maximum.
    """
    best_solution = None
    best_value = float('inf')  # Lower is better for misplaced tiles
    total_search_cost = 0
    restarts_used = 0

    for _ in range(max_restarts):
        restarts_used += 1
        initial_state = generate_random_puzzle()
        problem = EightPuzzle(initial_state)
        solution, search_cost = hill_climbing(problem)
        total_search_cost += search_cost
        solution_value = problem.value(solution)

        # If goal is found, return immediately
        if problem.goal_test(solution):
            return initial_state, solution, total_search_cost, restarts_used

        # Store the best solution seen so far
        if solution_value < best_value:
            best_solution = solution
            best_value = solution_value

    return initial_state, best_solution, total_search_cost, restarts_used

