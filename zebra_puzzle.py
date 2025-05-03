from csp import Zebra_candy, solve_zebra, backtracking_search, min_conflicts, AC3,forward_checking
import tkinter as tk

'''

Once again this is a work in progress. I grabbed the zebra problem and backtracking
min conflicts and AC3 algorithms from csp.py and created a class that solves the Zebra
problem. Its just passing the problem to the algorithms. 
'''


class ZebraSolver:
    def __init__(self):
        self.zebra_instance = Zebra_candy()

    #This def is solving with the backtracking algorithm
    def solve_with_backtracking(self):
        print("\n--- Solving with Backtracking Search ---")
        result = backtracking_search(self.zebra_instance)
        self.display_result(result, "Backtracking")
        return result

    #This def is solving with the min conflicts algorithm
    def solve_with_min_conflicts(self):
        print("\n--- Solving with Min Conflicts ---")
        zebra = Zebra_candy()
        # The steps here aid in solving with this algorithm
        #Represents the number of steps to solve it
        #Tbh this one im eh on cause its not solving it
        result = min_conflicts(zebra, max_steps=10000)
        self.display_result(result, "Min Conflicts")
        return result

    #This def solves with AC3
    def solve_with_ac3_backtracking(self):
        print("\n--- Solving with AC3 + Backtracking ---")
        # Fresh instance
        zebra = Zebra_candy()
        AC3(zebra)
        result = backtracking_search(zebra)
        self.display_result(result, "AC3 + Backtracking")
        return result

    def solve_with_forward_checking(self):
        print("\n--- Solving with Forward Checking ---")
        zebra = Zebra_candy()
        result = backtracking_search(zebra, inference=forward_checking)
        self.display_result(result, "Forward Checking")
        return result

    #Prints result on the terminal
    def display_result(self, result, method):
        if not result:
            print(f"{method} failed to find a solution.")
            return

        house_contents = {h: [] for h in range(1, 6)}
        color_map = {}
        zebra_house = None
        water_house = None

        for var, val in result.items():
            house_contents[val].append(var)
            if var in ['Red', 'Yellow', 'Blue', 'Green', 'Ivory']:
                color_map[val] = var
            if var == 'Zebra':
                zebra_house = val
            if var == 'Water':
                water_house = val

        self.show_gui(house_contents, color_map, zebra_house, water_house, title=method)

    #I kinda wanted to display the results as little houses cause im visual
    def show_gui(self, house_contents, color_map, zebra_house, water_house, title):
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

#Main function
if __name__ == '__main__':
    solver = ZebraSolver()
    solver.solve_with_backtracking()
    solver.solve_with_min_conflicts()
    solver.solve_with_ac3_backtracking()
    solver.solve_with_forward_checking()
