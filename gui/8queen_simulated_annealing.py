import os.path
import sys
import tkinter as tk  # Import tkinter for GUI display
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import Problem
from search import simulated_annealing_full  # Imported Simulated Annealing full

class NQueensProblem(Problem):
    """The problem of placing N queens on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    """

    def __init__(self, N):
        self.N = N
        self.initial = tuple([-1] * N)
        Problem.__init__(self, self.initial)

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] != -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        """Place the next queen at the given row."""
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)   # same / diagonal

    def goal_test(self, state):
        """Check if all columns filled, no conflicts."""
        if state[-1] == -1:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def h(self, node):  
        """Heuristic function for N-Queens problem for simulated annealing: 
        Number of conflicts (attacking queen pairs)."""    
        state = node.state
        num_conflicts = 0
        # Compare each pair of queens for conflicts
        for col1 in range(self.N):
            for col2 in range(col1 + 1, self.N):
                if self.conflict(state[col1], col1, state[col2], col2):  
                    num_conflicts += 1
        return num_conflicts
    
def create_board_display(solution, N):
    """Display the board with queens placed on it."""
    square_size = 50  # Size of each square
    board_size = N * square_size + 10
    color_counter = -1  

    window = tk.Tk()
    window.title(f"{N}-Queens Solution")
    canvas = tk.Canvas(window, width=board_size, height=board_size)
    canvas.pack()

    for row in range(N):
        for col in range(N):
            color_counter += 1
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size
            if solution[col] == row:
                color = "yellow"
            else:
                if(color_counter % 2 == 0): color = "white"
                else: color = "black"
            if(col == N-1): color_counter +=1

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if solution[col] == row:
                canvas.create_text(
                    x1 + square_size // 2, y1 + square_size // 2, 
                    text="Q", font=("Arial", 20, "bold"), fill="black"
                )

    window.mainloop()

if __name__ == "__main__":
    problem = NQueensProblem(8)
    solution, search_cost = simulated_annealing_full(problem)

    if problem.goal_test(solution[-1]):  # Use the last state in the list
        print("Solution Board:", solution[-1])
    else: 
        print("Failed Board:", solution[-1])

print(f"\nSearch Cost:", search_cost)
create_board_display(solution[-1], problem.N)
