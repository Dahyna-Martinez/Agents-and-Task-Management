from csp import Zebra_candy, solve_zebra, backtracking_search, min_conflicts, AC3,forward_checking
import tkinter as tk
import time

"""
Logic Puzzle Performance Report

This class defines the performance and efficiency metrics for the different algorithms of the logic puzzle. It specially denotes the final
status of the puzzle (Success or Failure), the execution time of the algorithm to solve the puzzle, and the amount of actions the 
algorithm required to do to attempt to solve the problem. The report for each algorithm is displayed in the terminal as each algorithm is executed.

"""

class PerformanceAndEfficiencyMetrics:
    """
        Defines the performance and efficiency metrics for
        the algorithms used to solve the logic puzzle and displays then within the terminal.

         Attributes:
             method (string): Name of the method used to solve the logic puzzle
             start (integer): Initial execution time before the algorithm is called
             end (integer): Execution time after the algorithm executes
             steps (integer): Total number of steps the algorithms traverses to solve the puzzle
             success (boolean): Determines if the algorithm is successful or not
    """
    def __init__(self, method_name):
        """
        Initializes the metrics and the display template.
        """
        self.method = method_name
        self.start = None
        self.end = None
        self.steps = 0
        self.success = False

    def start_timer(self):
        self.start = time.time()

    def end_timer(self):
        self.end = time.time()

    #Calculates the total execution time.
    def total_execution_time(self):
        if self.end:
            return round(self.end - self.start,4)
        else:
            return 0

    #Template set-up for the performance display.
    def metricsdisplay(self):
        print(f"\n- {self.method} Metric Report -")
        print(f"Status: {'Success' if self.success else 'Failure'}")
        print(f"Time: {self.total_execution_time()} seconds")
        print(f"Steps taken to solve problem: {self.steps}")

"""
Logic Puzzle Solver utilizing different CSP Algorithms

This class calls the different Constraint Satisfaction Problem to solve the Zebra Logic Problem.
It utilizes a specific list of constraints that is found within the csp.py.
"""
class ZebraSolver:

    """
    Defines an instances of the Zebra Logic Problem from the csp.py -> Zebra_candy() file.
    """
    def __init__(self):
        self.zebra_instance = Zebra_candy()


    """
    Primary logic for solving the Zebra Logic Problem.

    Operations include: calling the performance metrics, assigning the instance of
    the Backtracking Search algorithm, and displaying the results.

    Attributes:
        display_result(tkinter): Displays the results of the algorithm's execution in the terminal.
    """
    def solve_with_backtracking(self):
        """
        Defines an instances of the Zebra Logic Problem and assigns it to
        the Backtracking Algorithm. The algorithm attempts to solve the puzzle and
        display its results.
        """
        metrics = PerformanceAndEfficiencyMetrics("Backtracking")
        print("\n--- Solving with Backtracking Search ---")
        metrics.start_timer()
        # Calls the algorithm to solve the problem.
        result = backtracking_search(self.zebra_instance, metrics=metrics)
        metrics.end_timer()
        metrics.success = bool(result)
        self.display_result(result, metrics)
        return result


    def solve_with_min_conflicts(self):
        """
            Defines an instances of the Zebra Logic Problem and assigns it to
            the Min Conflict Algorithm. The algorithm attempts to solve the puzzle and
            display its results.
         """
        metrics = PerformanceAndEfficiencyMetrics("MinConflicts")
        print("\n--- Solving with Min Conflicts ---")
        zebra = Zebra_candy()
        metrics.start_timer()
        # Calls the algorithm to solve the problem.
        result = min_conflicts(zebra, max_steps=10000, metrics=metrics)
        metrics.end_timer()
        metrics.success = bool(result)
        self.display_result(result, metrics)
        return result


    def solve_with_ac3_backtracking(self):
        """
            Defines an instances of the Zebra Logic Problem and assigns it to
            the AC3 Algorithm. The algorithm attempts to solve the puzzle and
            display its results.
         """
        metrics = PerformanceAndEfficiencyMetrics("AC3 + Backtracking")
        print("\n--- Solving with AC3 + Backtracking ---")
        zebra = Zebra_candy()
        metrics.start_timer()
        # Calls the algorithm to solve the problem.
        AC3(zebra, metrics=metrics)
        result = backtracking_search(zebra, metrics=metrics)
        metrics.end_timer()
        metrics.success = bool(result)
        self.display_result(result, metrics)
        return result

    def solve_with_forward_checking(self):
        """
            Defines an instances of the Zebra Logic Problem and assigns it to
            the Forward Checking Algorithm. The algorithm attempts to solve the puzzle and
            display its results.
         """
        metrics = PerformanceAndEfficiencyMetrics("Forward Checking")
        print("\n--- Solving with Forward Checking ---")
        zebra = Zebra_candy()
        metrics.start_timer()
        # Calls the algorithm to solve the problem.
        result = backtracking_search(zebra, inference=forward_checking,metrics=metrics)
        metrics.end_timer()
        metrics.success = bool(result)
        self.display_result(result, metrics)
        return result

    """
      Prints the algorithm's results to the window.
    """
    def display_result(self, result,metrics):
        """
        Display's the solution of the puzzle onto the window. Identifies where the zebra and water are located.
        It shows which house, snack, drink, nationality, and pet each target is located.
        """
        metrics.metricsdisplay()
        if not result:
            return

        #Create the 5 different houses.
        house_contents = {h: [] for h in range(1, 6)}

        color_map = {}
        zebra_house = None
        water_house = None

         #Assigns the house colors, the zebra location and the water location.
        for var, val in result.items():
            house_contents[val].append(var)
            if var in ['Red', 'Yellow', 'Blue', 'Green', 'Ivory']:
                color_map[val] = var
            if var == 'Zebra':
                zebra_house = val
            if var == 'Water':
                water_house = val

        # Call that display's the answer on the window.
        self.show_gui(house_contents, color_map, zebra_house, water_house, title=metrics.method)

    """
    Creates the window interface that projects each algorithm's output into the screen.
    """
    def show_gui(self, house_contents, color_map, zebra_house, water_house, title):
        """
           Displays a graphical user interface (GUI) representing the five houses in the Zebra puzzle.

           Each house is drawn as a colored rectangle with its associated attributes (like nationality, drink, pet, etc.)
           listed inside. The house containing the zebra and the one with water are marked with emoji annotations.

           Attributes:
               house_contents dict[int, list[str]]: A dictionary mapping house numbers (1–5) to a list of assigned attributes for that house.

               color_map dict[int, str]:A mapping from house number to color name (e.g., "Red", "Green"), indicating the color of each house.

               zebra_house(integer): The house number that contains the zebra.

              water_house(integer): The house number that has water as the drink.

             title(string):Title to be displayed on the GUI window.

        """
        root = tk.Tk()
        root.title(title)

        canvas = tk.Canvas(root, width=1150, height=400, bg="white")
        canvas.pack()

        tk_colors = {
            "Red": "#FF6B6B",
            "Yellow": "#FFF176",
            "Blue": "#81D4FA",
            "Green": "#AED581",
            "Ivory": "#FFFFE0"
        }

        for i in range(5):
            x0 = 20 + i * 220
            y0 = 50
            x1 = x0 + 200
            y1 = y0 + 280
            house_num = i + 1
            color_name = color_map.get(house_num, None)
            color_fill = tk_colors.get(color_name, "#86B049")

            # Add emoji annotations
            emoji = ""
            if house_num == zebra_house:
                emoji += " 🦓"
            if house_num == water_house:
                emoji += " 💧"

            canvas.create_rectangle(x0, y0, x1, y1, fill=color_fill, outline="black", width=2)
            canvas.create_text((x0 + x1) / 2, y0 + 20, text=f"House {house_num}{emoji}", font=("Helvetica", 14, "bold"), anchor="n")
            items = sorted(house_contents[house_num])
            for j, item in enumerate(items):
                canvas.create_text((x0 + x1) / 2, y0 + 50 + j * 20, text=item, font=("Helvetica", 10))

        root.mainloop()

# Runs the application
if __name__ == '__main__':
    solver = ZebraSolver()
    solver.solve_with_backtracking()
    solver.solve_with_min_conflicts()
    solver.solve_with_ac3_backtracking()
    solver.solve_with_forward_checking()
