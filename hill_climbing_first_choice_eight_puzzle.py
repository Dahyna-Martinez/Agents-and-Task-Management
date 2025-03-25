from search import Problem

class FirstChoiceHillClimbingEightProblem(Problem):
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

    def __init__(self, initial, goal=None):
        """
               Initializes the 8-Puzzle problem with a given initial state and establishes a goal state.

               Parameters:
                   initial (tuple): A 3x3 puzzle state represented as a tuple of length 9.
               """
        super().__init__(initial, goal if goal is not None else (1, 2, 3, 4, 5, 6, 7, 8, 0))

    def actions(self, state):
        """
               Determines the possible moves based on the position of the empty tile (0).

               Parameters:
                   state (tuple): The current puzzle state.

               Returns:
                   list: A list of possible moves, chosen from ["UP", "DOWN", "LEFT", "RIGHT"].
               """
        actions = []
        # Finds the position of the empty space/tile (0)
        zero_pos = state.index(0)
        #Gahters the quotient and the remainder of the zero position divided by 3. Determines the row and columns.
        row, col = divmod(zero_pos, 3)

        # Determine possible moves
        if row > 0:
            #Allows upwards movements.
            actions.append('UP')
        if row < 2:
            # Allows downwards movements.
            actions.append('DOWN')
        if col > 0:
            # Allows movements to the left.
            actions.append('LEFT')
        if col < 2:
            # Allows movement to the right.
            actions.append('RIGHT')

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
        # Finds the position of the empty space/tile (0)
        zero_pos = state.index(0)
        # Converts the tuple to a list to allow modifications.
        new_state = list(state)

        if action == 'UP':
            new_zero_pos = zero_pos - 3
        elif action == 'DOWN':
            new_zero_pos = zero_pos + 3
        elif action == 'LEFT':
            new_zero_pos = zero_pos - 1
        elif action == 'RIGHT':
            new_zero_pos = zero_pos + 1

        # Swap the empty space (0) with the tile in the new position
        new_state[zero_pos], new_state[new_zero_pos] = new_state[new_zero_pos], new_state[zero_pos]

        return tuple(new_state)

    def goal_test(self, state):
        """Return True if the state is the goal state."""
        return state == self.goal

    def value(self, state):
        """
               Calculates the Manhattan Heuristic values. It evaluates the state based on the sum of Manhattan
               distances from their positions in the goal states.
                A value closer to 0 indicates a better state.

            Parameters:
                state (tuple): The state of the puzzle as a tuple of integers.

            Returns:
                int: The sum of the Manhattan distances excluding the blank tile.
            """
        manhattan_distance = 0
        # Loops through all 9 positions.
        for i in range(9):
            # Skips the blank tile.
            if state[i] != 0:
                # Find the target position of the tile in the goal state.
                target_row, target_col = divmod(self.goal.index(state[i]), 3)
                current_row, current_col = divmod(i, 3)

                # Adds the Manhattan distance for the tile.
                manhattan_distance += abs(current_row - target_row) + abs(current_col - target_col)

        return manhattan_distance

    def path_cost(self, cost, state1, action, state2):
        """Return the cost of taking an action from one state to another, always 1."""
        # Accumulate path cost.
        return cost + 1
