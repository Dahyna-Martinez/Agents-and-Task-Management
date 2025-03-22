import random
from search import Problem


class EightPuzzleProblem(Problem):
    """
    8-Puzzle problem implementation for hill climbing.
    The puzzle consists of a 3x3 grid with tiles numbered 1 to 8 and a blank space (0).
    The goal is to arrange the tiles in order from left to right, top to bottom.

    Attributes:
        initial (tuple): The starting state of the puzzle represented as a tuple of 9 integers.

    Methods:
        actions(state): Returns the possible moves (up, down, left, right).
        result(state, action): Returns the new state after applying an action.
        value(state): Computes the heuristic value based on misplaced tiles.
    """

    def __init__(self, initial):
        """
        Initializes the 8-Puzzle problem with a given initial state.

        Parameters:
            initial (tuple): A 3x3 puzzle state represented as a tuple of length 9.
        """
        super().__init__(initial)

    def actions(self, state):
        """
        Determines the possible moves based on the position of the empty tile (0).

        Parameters:
            state (tuple): The current puzzle state.

        Returns:
            list: A list of possible moves, chosen from ["UP", "DOWN", "LEFT", "RIGHT"].
        """
        empty_index = state.index(0)
        row, col = divmod(empty_index, 3)  # Convert index to (row, col) coordinates
        actions = []

        if row > 0: actions.append("UP")
        if row < 2: actions.append("DOWN")
        if col > 0: actions.append("LEFT")
        if col < 2: actions.append("RIGHT")

        return actions

    def result(self, state, action):
        """
        Generates the new state after applying the given action.

        Parameters:
            state (tuple): The current puzzle state.
            action (str): The move to be applied (one of "UP", "DOWN", "LEFT", "RIGHT").

        Returns:
            tuple: The new state after swapping the empty tile (0) with its adjacent tile.
        """
        empty_index = state.index(0)
        new_state = list(state)  # Convert tuple to list for mutability

        def swap(i, j):
            """ Helper function to swap two elements in the state list. """
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
        """
        Heuristic function that evaluates the state based on the number of misplaced tiles.
        A higher value (closer to 0) indicates a better state.

        Parameters:
            state (tuple): The current puzzle state.

        Returns:
            int: The negative count of misplaced tiles (-1 per misplaced tile),
                 so that the algorithm maximizes the score.
        """
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Goal state
        return -sum(s != g for s, g in zip(state, goal))  # Negative for maximization


def generate_random_puzzle():
    """
    Generates a solvable random 8-Puzzle instance by shuffling the tiles.

    Returns:
        tuple: A randomly shuffled 8-puzzle state.
    """
    puzzle = list(range(9))
    random.shuffle(puzzle)
    return tuple(puzzle)


if __name__ == "__main__":
    # Create a new 8-Puzzle problem with a randomly generated initial state
    problem = EightPuzzleProblem(generate_random_puzzle())

    # Print initial puzzle state and heuristic value
    print("Initial State:", problem.initial)
    print("Misplaced Tiles Heuristic Value:", problem.value(problem.initial))
