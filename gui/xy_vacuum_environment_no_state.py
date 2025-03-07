import os.path
from tkinter import *
import random
import sys

from networkx.algorithms.efficiency_measures import efficiency

from agents import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Gui(VacuumEnvironment):
    """This is a two-dimensional GUI environment. Each location may be
    dirty, clean or can have a wall. The user can change these at each step.

    Attributes:
        Environment (class): Establishes a GUI environment,
        where each location or tile may be clean, dirty, or a wall.

    """
    xi, yi = (0, 0)
    perceptible_distance = 1

    def __init__(self, root, width=7, height=7, elements=None):
        """
                 Initializes the GUI environment object.
                        Parameters:
                            root (str): Stores the main tkinter window that allows to create and manage GUI elements.
                            height (int): The height of the GUI window.
                            width(int): The width of the GUI window.
                            elements(list): Stores the elements of the GUI window.

                """
        super().__init__(width, height)
        """Stores whether initially each location is Clean or Dirty."""
        if elements is None:
            elements = ['D', 'W']
        self.root = root
        self.create_frames()
        self.create_buttons()
        self.create_walls()
        self.elements = elements

        #Keeps track of moves for the vacuum agent and displays it
        self.move_count=0
        self.move_label = Label (self.root, text=f"Moves: {self.move_count}", font=("Courier", 10))
        self.move_label.pack(side= 'left', anchor='w', padx= 10, pady= 5)

        #Keeps track of performance for the vacuum agent and displays it
        self.performance_score = 0
        self.performance_label = Label(self.root, text=f"Performance: {self.performance_score}", font=("Courier", 10))
        self.performance_label.pack(side='left', anchor='w', padx=10, pady=5)

        #Keep track of dirt cleaned by the vacuum agent
        self.dirt_cleaned = 0
        self.efficiency_label = Label(self.root, text=f"Efficiency: 0%", font=("Courier", 10))
        self.efficiency_label.pack(side='left', anchor='w', padx=10, pady= 5)


    def create_frames(self):
        """
        Adds frames to the GUI environment.
        """
        self.frames = []
        for _ in range(7):
            frame = Frame(self.root, bg='grey')
            frame.pack(side='bottom')
            self.frames.append(frame)

    def create_buttons(self):
        """
        Adds buttons to the respective frames in the GUI.
        """
        self.buttons = []
        for frame in self.frames:
            button_row = []
            for _ in range(7):
                button = Button(frame, height=3, width=5, padx=2, pady=2)
                button.config(
                    command=lambda btn=button: self.display_element(btn))
                button.pack(side='left')
                button_row.append(button)
            self.buttons.append(button_row)

    def create_walls(self):
        """
        Creates the outer boundary walls which do not move.
        """
        for row, button_row in enumerate(self.buttons):
            if row == 0 or row == len(self.buttons) - 1:
                for button in button_row:
                    button.config(text='W', state='disabled',
                                  disabledforeground='black')
            else:
                button_row[0].config(
                    text='W', state='disabled', disabledforeground='black')
                button_row[len(button_row) - 1].config(text='W',
                                                       state='disabled', disabledforeground='black')
        # Place the agent in the centre of the grid.
        self.buttons[3][3].config(
            text='A', state='disabled', disabledforeground='black')

    def display_element(self, button):
        """
        Show the things on the GUI.
        Parameters:
            button (button): The button used to display the element. Changes on clicks by the user.
        """
        txt = button['text']
        if txt != 'A':
            if txt == 'W':
                button.config(text='D')
            elif txt == 'D':
                button.config(text='')
            elif txt == '':
                button.config(text='W')

    def execute_action(self, agent, action):
        """
                Change the location status (Dirty/Clean); track performance.
                Score 100 for each dirt cleaned; -1 for each move.
                Also keeps track of dirt cleaned by adding +1

                Parameters:
                   agent (Agent): The vacuum agent.
                   action(str): The action that the agent performs ('Right', 'Left', 'Suck', 'Noop').

                """
        xi, yi = (self.xi, self.yi)
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list:
                dirt = dirt_list[0]
                agent.performance += 100
                self.dirt_cleaned += 1
                self.delete_thing(dirt)
                self.buttons[xi][yi].config(text='', state='normal')
                xf, yf = agent.location
                self.buttons[xf][yf].config(
                    text='A', state='disabled', disabledforeground='black')

        else:
            agent.bump = False
            if action == 'TurnRight':
                agent.direction += Direction.R
            elif action == 'TurnLeft':
                agent.direction += Direction.L
            elif action == 'Forward':
                agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
                if not agent.bump:
                    self.buttons[xi][yi].config(text='', state='normal')
                    xf, yf = agent.location
                    self.buttons[xf][yf].config(
                        text='A', state='disabled', disabledforeground='black')

        if action != 'NoOp':
            agent.performance -= 1
            self.move_count += 1
            self.update_labels()
            self.move_label.config(text=f"Moves: {self.move_count}")

        self.performance_score = agent.performance
        self.performance_label.config(text=f"Performance: {self.performance_score}")

    def update_labels(self):
        """Update the performance, move count, and efficiency labels."""
        efficiency = (self.dirt_cleaned / self.move_count) * 100 if self.move_count > 0 else 0
        self.move_label.config(text=f"Moves: {self.move_count}")
        self.performance_label.config(text=f"Performance: {self.performance_score}")
        self.efficiency_label.config(text=f"Efficiency: {efficiency:.2f}%")

    def read_env(self):
        """Reads the current state of the GUI environment."""
        for i, btn_row in enumerate(self.buttons):
            for j, btn in enumerate(btn_row):
                if (i != 0 and i != len(self.buttons) - 1) and (j != 0 and j != len(btn_row) - 1):
                    agt_loc = self.agents[0].location
                    if self.some_things_at((i, j)) and (i, j) != agt_loc:
                        for thing in self.list_things_at((i, j)):
                            self.delete_thing(thing)
                    if btn['text'] == self.elements[0]:
                        self.add_thing(Dirt(), (i, j))
                    elif btn['text'] == self.elements[1]:
                        self.add_thing(Wall(), (i, j))

    def update_env(self):
        """Updates the GUI environment according to the current state."""
        self.read_env()
        agt = self.agents[0]
        previous_agent_location = agt.location
        self.xi, self.yi = previous_agent_location
        self.step()
        xf, yf = agt.location

    def reset_env(self, agt):
        """Resets the GUI environment to the initial state.

        Parameters:
            agt (object): The agent that will be placed in the environment.
                  It should have a `performance` attribute that is reset to 0.

        """
        self.read_env()
        for i, btn_row in enumerate(self.buttons):
            for j, btn in enumerate(btn_row):
                if (i != 0 and i != len(self.buttons) - 1) and (j != 0 and j != len(btn_row) - 1):
                    if self.some_things_at((i, j)):
                        for thing in self.list_things_at((i, j)):
                            self.delete_thing(thing)
                            btn.config(text='', state='normal')
        self.add_thing(agt, location=(3, 3))
        self.buttons[3][3].config(
            text='A', state='disabled', disabledforeground='black')

        self.move_count = 0
        self.move_label.config(text=f"Moves: {self.move_count}")

        agt.performance = 0
        self.performance_score = 0
        self.performance_label.config(text=f"Performance: {self.performance_score}")
        self.dirt_cleaned = 0
        self.move_count=0
        self.efficiency_label.config(text=f"Efficiency: 0.00%")



def XYReflexAgentProgram(percept):
    """
        The modified SimpleReflexAgentProgram for the GUI environment.

        Parameters:
        percept (tuple): A tuple containing two elements:
            - status (str): 'Clean' or 'Dirty', indicating the status of the current tile.
            - bump (str): 'Bump' if the agent has hit a wall, otherwise an empty string.

        Returns:
        str: An action to be performed by the agent:
            - 'Suck' if the current tile is dirty.
            - 'TurnRight' or 'TurnLeft' if the agent randomly decides to turn.
            - 'Forward' if the agent moves ahead.
        """
    status, bump = percept
    if status == 'Dirty':
        return 'Suck'

    if bump == 'Bump':
        value = random.choice((1, 2))
    else:
        value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

    if value == 1:
        return 'TurnRight'
    elif value == 2:
        return 'TurnLeft'
    else:
        return 'Forward'


class XYReflexAgent(Agent):
    """
        The modified SimpleReflexAgent for the GUI environment.

        Attributes:
        location (tuple): The initial position of the agent in the grid (default is (3,3)).
        direction (Direction): The initial direction of the agent (default is "up").

         Args:
        program (function, optional): The agent's decision-making function that determines actions based on percepts.

        """

    def __init__(self, program=None):
        """
                Initializes the XYReflexAgent with a default location and direction.

                Parameters:
                program (function, optional): The decision-making function for the agent.
                                              Defaults to None, in which case the superclass handles it.
                """
        super().__init__(program)
        self.location = (3, 3)
        self.direction = Direction("up")

def auto_run():
    """
        Automatically runs the environment simulation by executing steps at regular intervals.

        The simulation stops if either of the following conditions is met:
        - The number of cleaned dirt patches reaches 18.
        - The agent has moved 500 times.

        Otherwise, it updates the environment and schedules the next step after 500 milliseconds.
        """
    if env.dirt_cleaned >= 18 or env.move_count >= 500:#change the amount of dirt for different test
        return  # Stop execution
    env.update_env()  # Perform one step
    root.after(500, auto_run)  # Repeat after 200 milliseconds (adjust the delay if needed)

# TODO: Check the coordinate system.
# TODO: Give manual choice for agent's location.
if __name__ == "__main__":
    root = Tk()
    root.title("Vacuum Environment")
    root.geometry("420x490")
    root.resizable(0, 0)
    frame = Frame(root, bg='black')
    reset_button = Button(frame, text='Reset', height=2,
                          width=6, padx=2, pady=2)
    reset_button.pack(side='left')
    next_button = Button(frame, text='Next', height=2,
                         width=6, padx=2, pady=2)
    next_button.pack(side='left')
    auto_button = Button(frame, text='Auto', height=2, width=6, padx=2, pady=2)
    auto_button.pack(side='left')
    frame.pack(side='bottom')
    env = Gui(root)
    agt = XYReflexAgent(program=XYReflexAgentProgram)
    env.add_thing(agt, location=(3, 3))
    next_button.config(command=env.update_env)
    reset_button.config(command=lambda: env.reset_env(agt))
    auto_button.config(command=lambda: auto_run())
    root.mainloop()
