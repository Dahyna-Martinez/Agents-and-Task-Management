from search import breadth_first_tree_search, MissionariesCannibals  # BFS
import tkinter as tk
from tkinter import ttk, messagebox
# Create an instance of the problem

class MissionariesCannibalsGUI:
    def __init__(self, root, solution):
        self.root = root
        self.solution = solution
        self.step = 0
        self.history = []  # Stores previous steps
        self.root.title("Missionaries and Cannibals")
        self.root.geometry("800x400")  # Set initial window size
        self.root.resizable(True, True)  # Make the window resizable

        # Layout
        self.left_bank_label = tk.Label(root, text="", font=("Arial", 14), width=30)
        self.left_bank_label.grid(row=0, column=0, padx=20, pady=5)

        self.boat_label = tk.Label(root, text="", font=("Arial", 14), width=15, bg="yellow")
        self.boat_label.grid(row=0, column=1, padx=10, pady=5)

        self.right_bank_label = tk.Label(root, text="", font=("Arial", 14), width=30)
        self.right_bank_label.grid(row=0, column=2, padx=20, pady=5)

        # Scrollable History Frame
        history_frame = tk.Frame(root)
        history_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        self.history_text = tk.Text(history_frame, height=10, width=80, state=tk.DISABLED, font=("Arial", 12), wrap="word")
        self.history_scroll = ttk.Scrollbar(history_frame, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=self.history_scroll.set)

        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Control buttons
        self.next_button = ttk.Button(root, text="Next Step", command=self.next_step)
        self.next_button.grid(row=2, column=1, pady=10)

        # Adjust row & column weights for resizing
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Initialize the display
        self.update_display()

    def update_display(self):
        """Update the text representation of the river banks, boat, and history."""
        if self.step < len(self.solution):
            state = self.solution[self.step]
            m_left, c_left, boat, m_right, c_right = state
            boat_position = "←" if boat == 1 else "→"

            # Update labels
            self.left_bank_label.config(text=f"Left Bank: {m_left}M, {c_left}C")
            self.boat_label.config(text=f"Boat {boat_position}")
            self.right_bank_label.config(text=f"Right Bank: {m_right}M, {c_right}C")

            # Add step to history
            self.history.append(f"Step {self.step}: {m_left}M, {c_left}C | {boat_position} | {m_right}M, {c_right}C")

            # Update history text box
            self.history_text.config(state=tk.NORMAL)  # Enable editing
            self.history_text.insert(tk.END, self.history[-1] + "\n")  # Add new step
            self.history_text.config(state=tk.DISABLED)  # Disable editing again
            self.history_text.yview_moveto(1.0)  # Auto-scroll to the bottom

    def next_step(self):
        """Move to the next step in the solution."""
        if self.step < len(self.solution) - 1:
            self.step += 1
            self.update_display()
        else:
            self.next_button.config(state=tk.DISABLED)
            messagebox.showinfo("Finished", "Solution Completed!")


# Example solution path (Replace with actual computed solution)
if __name__ == "__main__":
    from search import breadth_first_tree_search, MissionariesCannibals, depth_first_tree_search, depth_limited_search

    # Solve the problem
    problem = MissionariesCannibals()
    solution_node = breadth_first_tree_search(problem)
    #solution_node=depth_limited_search(problem)
    # Extract solution path
    solution_path = [node.state for node in solution_node.path()]

    root = tk.Tk()
    app = MissionariesCannibalsGUI(root, solution_path)
    root.mainloop()
