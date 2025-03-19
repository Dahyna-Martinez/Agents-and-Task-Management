import tkinter as tk
import tkinter.simpledialog as simpledialog
from queue import PriorityQueue
from tkinter import ttk


class Node:
    """Class to represent a cell in the grid for pathfinding."""

    def __init__(self, state, parent=None):
        self.state = state  # This holds the coordinate (x, y)
        self.parent = parent  # Reference to the parent Node
        self.g = 0  # Cost from start to this node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __lt__(self, other):
        return self.f < other.f

    def expand(self, app):
        """Expand the current node to return all valid neighbors."""
        neighbors = []
        x, y = self.state
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            new_state = (x + dx, y + dy)
            if 0 <= new_state[0] < app.grid_size and 0 <= new_state[1] < app.grid_size:
                # Check if the new state is not a wall and is not already explored
                if app.grid_cells[new_state[0]][new_state[1]].cget("text") != 'Wall':  # Not an obstacle
                    neighbors.append(Node(new_state, self))
        return neighbors


class SearchGrid(tk.Tk):
    def __init__(self, grid_size=20):
        super().__init__()
        self.title("Grid Pathfinding")
        self.grid_size = grid_size
        self.grid_cells = []
        self.start = None
        self.goal = None
        self.create_grid()
        self.create_control_buttons()
        self.switched = False

    def create_grid(self):
        """Creates the grid of buttons."""
        for i in range(self.grid_size):
            row = []
            self.grid_rowconfigure(i, weight=1)  # Allow row to expand
            for j in range(self.grid_size):
                self.grid_columnconfigure(j, weight=1)  # Allow column to expand
                btn = ttk.Button(self, text=f"({i}, {j})", command=lambda x=i, y=j: self.toggle_cell(x, y))
                btn.grid(row=i, column=j, sticky="nsew")  # Fill the whole cell
                row.append(btn)
            self.grid_cells.append(row)

    def create_control_buttons(self):
        """Creates the buttons under the grid for functionality."""
        control_frame = tk.Frame(self)
        control_frame.grid(row=self.grid_size, column=0, columnspan=self.grid_size, sticky="ew")

        # Creation of Buttons
        ttk.Button(control_frame, text="Set Start", command=self.set_start).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Set Goal", command=self.set_goal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Find Path", command=self.find_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Coodinates On/Off", command=self.show_coordinates).pack(side=tk.LEFT, padx=5)

    def toggle_cell(self, x, y):
        """Toggle the state of the grid cell."""
        current_text = self.grid_cells[x][y].cget("text")

        if current_text == f"({x}, {y})":
            self.grid_cells[x][y].config(text='Wall')

        elif current_text == '':
            self.grid_cells[x][y].config(text='Wall')

        else:
            if not self.switched:
                self.grid_cells[x][y].config(text=f"({x}, {y})")
            else:
                self.grid_cells[x][y].config(text='')

    def set_start(self):
        """Set the start cell."""
        if self.start:
            x, y = self.start
            self.grid_cells[self.start[0]][self.start[1]].config(text=f"({x}, {y})")  # Clear previous start
        self.start = self.get_cell()
        if self.start:
            x, y = self.start
            self.grid_cells[x][y].config(text='Start')  # Mark as start

    def set_goal(self):
        """Set the goal cell."""
        if self.goal:
            x, y = self.goal
            self.grid_cells[self.goal[0]][self.goal[1]].config(text=f"({x}, {y})")  # Clear previous goal
        self.goal = self.get_cell()
        if self.goal:
            x, y = self.goal
            self.grid_cells[x][y].config(text='Goal')  # Mark as goal

    def get_cell(self):
        """Simple prompt to select a cell."""
        response = simpledialog.askstring("Select Cell", "Enter cell (row,column):")
        if response:
            try:
                # Attempt to convert the response into two integers (x, y)
                x, y = map(int, response.split(','))

                # Check if the cell is within the valid grid range
                if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                    return (x, y)
                else:
                    tk.messagebox.showwarning("Warning", "That Cell Does Not Exist")  # Out of bounds

            except ValueError:
                # Handle the case where the user input is not valid integers
                tk.messagebox.showwarning("Warning", "Invalid input!")

        return None

    def straight_line_distance(self, A, B):
        "Straight-line distance between two points."
        return sum(abs(a - b) ** 2 for (a, b) in zip(A, B)) ** 0.5

    def heuristic(self, node):
        "Straight-line distance between state and the goal."
        return self.straight_line_distance(node.state, self.goal)

    def Astar(self):
        if not self.start or not self.goal:
            tk.messagebox.showwarning("Warning", "Start or goal not set!")
            return

        frontier = PriorityQueue()
        start_node = Node(self.start)
        frontier.put((0, start_node))
        explored = set()

        while not frontier.empty():
            current_node = frontier.get()[1]

            # Check if the goal was reached
            if current_node.state == self.goal:
                self.reconstruct_path(current_node, "A*")
                return

            explored.add(current_node.state)

            for child in current_node.expand(self):
                if child.state in explored:
                    continue

                child.g = current_node.g + 1
                child.h = self.heuristic(child)
                child.f = child.g + child.h

                # Only add if not already in frontier
                already_in_frontier = False
                for item in frontier.queue:
                    if item[1] == child and item[1].f <= child.f:
                        already_in_frontier = True
                        break

                if not already_in_frontier:
                    frontier.put((child.f, child))

        tk.messagebox.showinfo("Result", "No path found!")

    def GreedyBFS(self):
        if not self.start or not self.goal:
            tk.messagebox.showwarning("Warning", "Start or goal not set!")
            return

        frontier = PriorityQueue()
        start_node = Node(self.start)
        frontier.put((0, start_node))  # Starting node
        explored = set()

        while not frontier.empty():
            current_node = frontier.get()[1]

            # Check if we reach the goal
            if current_node.state == self.goal:
                self.reconstruct_path(current_node, "Greedy")
                return

            explored.add(current_node.state)

            for child in current_node.expand(self):
                if child.state not in explored:
                    child.h = self.heuristic(child)  # Greedy BFS only uses heuristic
                    child.f = child.h  # f = h
                    frontier.put((child.f, child))

        tk.messagebox.showinfo("Result", "No path found!")

    def find_path(self):

        algorithms = ["A*", "Greedy BFS"]
        selected_algorithm = tk.StringVar(value=algorithms[0])

        dialog = tk.Toplevel(self)
        dialog.title("Select Algorithm")
        dialog.geometry("250x150")

        tk.Label(dialog, text="Choose an Algorithm:").pack(pady=5)

        for algo in algorithms:
            tk.Radiobutton(dialog, text=algo, variable=selected_algorithm, value=algo).pack(anchor="w")

        def confirm_selection():
            algorithm = selected_algorithm.get()
            tk.messagebox.showinfo("Algorithm Selected", f"Using {algorithm} for pathfinding!")
            dialog.destroy()
            if algorithm == "A*":
                self.Astar()
            elif algorithm == "Greedy BFS":
                self.GreedyBFS()

        ttk.Button(dialog, text="OK", command=confirm_selection).pack(pady=10)

    def reset(self):
        """Resets the grid, start, and goal positions."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.grid_cells[x][y].config(text=f"({x}, {y})")  # Clear all cell labels

        self.start = None
        self.goal = None

    def show_coordinates(self):
        if self.switched == False:
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if (x, y) != self.start and (x, y) != self.goal and self.grid_cells[x][y].cget("text") != 'Wall':
                        self.grid_cells[x][y].config(text='')
            self.switched = True
        else:
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if (x, y) != self.start and (x, y) != self.goal and self.grid_cells[x][y].cget("text") != 'Wall':
                        self.grid_cells[x][y].config(text=f"({x}, {y})")
            self.switched = False

    def reconstruct_path(self, current, algorithm):
        """Reconstructs the path to the goal."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) != self.start and (x, y) != self.goal and self.grid_cells[x][y].cget("text") != 'Wall':
                    self.grid_cells[x][y].config(text='')
        path = []
        while current is not None:
            x, y = current.state

            # Skip start and goal cells
            if (x, y) != self.start and (x, y) != self.goal:
                if algorithm == "A*":
                    self.grid_cells[x][y].config(text="A*")  # Mark the path in "A*" if A* is used
                else:
                    self.grid_cells[x][y].config(text='G')  # Mark the path in 'G' if Greedy BFS is used

                path.append((x, y))

            current = current.parent

        path.reverse()
        print("\nPath to the goal:", path)


if __name__ == "__main__":
    app = SearchGrid(grid_size=20)  # Grid size
    app.geometry('1280x720')
    app.mainloop()