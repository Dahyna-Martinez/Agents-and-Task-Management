import os.path
import sys
import tkinter as tk
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import Problem
from search import simulated_annealing_full  # Imported simulated annealing full

class NQueensProblemV2(Problem):
    """The problem of placing N queens on an NxN board with none attacking each other."""
    
    def __init__(self, N):
        self.N = N
        self.initial = self.generate_random_state()  # Generate a random initial state
        Problem.__init__(self, self.initial)

    def generate_random_state(self):
        """Generate a random initial state with all queens placed."""
        return tuple(random.sample(range(self.N), self.N))  # A permutation of (0,1,...,N-1)

    def actions(self, state):
        """Find all possible moves (swaps between two rows)."""
        actions = []
        for col1 in range(self.N):
            for col2 in range(col1 + 1, self.N):
                actions.append((col1, col2))  # Swap queens in columns col1 and col2
        return actions

    def result(self, state, action):
        """Swap two columns' queen positions to generate a new state."""
        col1, col2 = action
        new_state = list(state)
        new_state[col1], new_state[col2] = new_state[col2], new_state[col1]
        return tuple(new_state)

    def conflicted(self, state, row, col):
        """Check if a queen at (row, col) is in conflict with others."""
        return any(self.conflict(row, col, state[c], c) for c in range(self.N) if c != col)

    def conflict(self, row1, col1, row2, col2):
        """Check if two queens are in conflict."""
        return row1 == row2 or abs(row1 - row2) == abs(col1 - col2)

    def goal_test(self, state):
        """Check if the state is a valid N-Queens solution."""
        return all(not self.conflicted(state, state[col], col) for col in range(self.N))

    def h(self, node):
        """Heuristic: Count the number of conflicts in the board."""
        state = node.state
        return sum(self.conflict(state[col1], col1, state[col2], col2)
                   for col1 in range(self.N) for col2 in range(col1 + 1, self.N))

def create_board_display():
    """Initialize the GUI board."""
    global canvas, window, result_label
    square_size = 50
    board_size = N * square_size + 10

    window = tk.Tk()
    window.title(f"{N}-Queens Problem")
    canvas = tk.Canvas(window, width=board_size, height=board_size)
    canvas.pack()

    # Solve button
    solve_button = tk.Button(window, text="Solve", command=solve_problem, font=("Arial", 12))
    solve_button.pack()

    # Label for displaying results
    result_label = tk.Label(window, text="", font=("Arial", 12))
    result_label.pack()

    update_board(problem.initial)  # Display initial board

    window.mainloop()

def update_board(state):
    """Update the board display with the given state."""
    square_size = 50
    canvas.delete("all")  # Clear previous board
    for row in range(N):
        for col in range(N):
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size
            if state[col] == row:
                color = "yellow"
            else: color = "white" if (row + col) % 2 == 0 else "black"                            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if state[col] == row:                
                canvas.create_text(
                    x1 + square_size // 2, y1 + square_size // 2,
                    text="Q", font=("Arial", 20, "bold"), fill="black",                    
                )

def solve_problem():
    """Solve the N-Queens problem and update the board."""
    global solution, search_cost
    solution, search_cost = simulated_annealing_full(problem)  
    final_state = solution[-1]  # Get the last state in the solution list

    update_board(final_state)  # Update board to show solution

    if problem.goal_test(final_state):
        result_text = f"Solution Found: {final_state}"
    else:
        result_text = f"No Solution Found: {final_state}"

    print(result_text)  
    print(f"Search Cost: {search_cost}")  

    result_label.config(text=result_text)  # Update GUI result label

if __name__ == "__main__":
    N = 8  # Number of queens
    problem = NQueensProblemV2(N)
    create_board_display()
