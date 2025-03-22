import random
from search import Problem


class EightPuzzleProblem(Problem):
    """ 8-Puzzle problem for hill climbing. """

    def __init__(self, initial):
        super().__init__(initial)

    def actions(self, state):
        """ Returns the possible moves (up, down, left, right). """
        empty_index = state.index(0)
        row, col = divmod(empty_index, 3)
        actions = []

        if row > 0: actions.append("UP")
        if row < 2: actions.append("DOWN")
        if col > 0: actions.append("LEFT")
        if col < 2: actions.append("RIGHT")

        return actions

    def result(self, state, action):
        """ Returns the new state after applying an action. """
        empty_index = state.index(0)
        new_state = list(state)

        def swap(i, j):
            new_state[i], new_state[j] = new_state[j], new_state[i]

        if action == "UP":
            swap(empty_index, empty_index - 3)
        elif action == "DOWN":
            swap(empty_index, empty_index + 3)
        elif action == "LEFT":
            swap(empty_index, empty_index - 1)
        elif action == "RIGHT":
            swap(empty_index, empty_index + 1)

        return tuple(new_state)

    def value(self, state):
        """ Heuristic: Counts misplaced tiles. """
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        return -sum(s != g for s, g in zip(state, goal))  # Negative for maximization


def generate_random_puzzle():
    """ Generates a solvable random 8-puzzle instance. """
    puzzle = list(range(9))
    random.shuffle(puzzle)
    return tuple(puzzle)


if __name__ == "__main__":
    problem = EightPuzzleProblem(generate_random_puzzle())
    print("Initial State:", problem.initial)
    print("Misplaced Tiles Heuristic Value:", problem.value(problem.initial))
