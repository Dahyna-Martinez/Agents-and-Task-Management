import os.path
import sys
from tkinter import *

from agents import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# The two locations for the Vacuum world
loc_A, loc_B = (0, 0), (1, 0)


class Gui(Environment):
    """
    This GUI environment has two locations, A and B. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status.

    Attributes:
        Environment (class): Establishes a GUI environment,
        where each location or tile may be clean, dirty, or a wall.

    """

    def __init__(self, root, height=300, width=380):
        """
         Initializes the GUI environment object.
                Parameters:
                    root (str): Stores the main tkinter window that allows to create and manage GUI elements.
                    height (int): The height of the GUI window.
                    width(int): The width of the GUI window.

        """
        super().__init__()
        """Stores whether initially each location is Clean or Dirty."""
        self.status = {loc_A: 'Clean',
                       loc_B: 'Clean'}
        self.root = root
        self.height = height
        self.width = width
        #Initialized GUI components
        self.canvas = None
        self.buttons = []
        self.create_canvas()
        self.create_buttons()
        #Added performance measurements
        self.performance_label= None
        self.create_performance_title()
        self.create_performance_info()

        #Total dirt cleaned counter
        self.dirt_cleaned= 0
        #Total steps counter
        self.total_steps = 0

    def thing_classes(self):
        """
        Defines the agents and objects that are
        allowed to be used within the environment.

        Returns:
           List of agent and object classes.
        """
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """
        Defines what the agent's current location and its cleanliness status.
        Parameters:
            agent (Agent): Vacuum agent that perceives its location.

        Returns:
           The status of the agent's current location and the location's status.

        """
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        """
        Change the location status (Dirty/Clean); track performance.
        Score 10 for each dirt cleaned; -1 for each move.

        Parameters:
           agent (Agent): The vacuum agent.
           action(str): The action that the agent performs ('Right', 'Left', 'SucK').

        """
        self.total_steps  += 1

        if action == 'Right':
            agent.location = loc_B
            agent.performance -= 1
        elif action == 'Left':
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                self.dirt_cleaned += 1
                if agent.location == loc_A:
                    self.buttons[0].config(bg='white', activebackground='light grey')
                else:
                    self.buttons[1].config(bg='white', activebackground='light grey')
                agent.performance += 10
            self.status[agent.location] = 'Clean'
        self.update_performance_title(agent)

    def default_location(self, thing):
        """
        Determines randomly the starting location of the agent on the grid.

        Parameters:
            thing (Agent): The vacuum agent, to be placed.

        Returns:
            A randomly assigned row and column location.

        """
        return random.choice([loc_A, loc_B])

    def create_canvas(self):
        """Creates Canvas element in the GUI. """
        self.canvas = Canvas(
            self.root,
            width=self.width,
            height=self.height,
            background='light grey')
        self.canvas.pack(side='bottom')
        #Adds a text in the canvas tha explains the performance measurement
        self.performance_info_text = self.canvas.create_text(
            190, 50, text="Performance: +10 per dirt cleaned, -1 per move\n"
                          "Effectivity: Dirt cleaned / Steps taken",
            font=("Courier", 10, "italic"), fill="black"
        )

    def create_buttons(self):
        """Creates the buttons required in the GUI."""
        button_left = Button(self.root, height=4, width=12, padx=2, pady=2, bg='white')
        button_left.config(command=lambda btn=button_left: self.dirt_switch(btn))
        self.buttons.append(button_left)
        button_left_window = self.canvas.create_window(130, 200, anchor=N, window=button_left)
        button_right = Button(self.root, height=4, width=12, padx=2, pady=2, bg='white')
        button_right.config(command=lambda btn=button_right: self.dirt_switch(btn))
        self.buttons.append(button_right)
        button_right_window = self.canvas.create_window(250, 200, anchor=N, window=button_right)

    def create_performance_title(self):
        """Creates a title for the Performance meter to be displayed"""
        self.performance_label = Label(self.root,text="Performance: 0", font=("Courier", 12))
        self.performance_label.pack(side='top',pady=5)
        self.performance_info = Label(self.root, text="+10 per dirt cleaned, -1 per move",
                                      font=("Courier", 10, "bold"), fg="black")
        self.performance_info.pack(side='top')


    def update_performance_title(self, agent):
        """
        Updates the title of the Performance meter to be displayed.
        Parameters:
            agent (Agent): The vacuum agent.
            """
        if self.total_steps > 0:
            effectivity= (self.dirt_cleaned/ self.total_steps) *100
        else:
            effectivity= 0

        self.performance_label.config(text=f"Performance: {agent.performance} Effectivity: {effectivity: .2f}")

    def dirt_switch(self, button):
        """
        Gives user the option to put dirt in any tile.

        Parameters:
            button (Button): The button that allows to toggle the dirt on or off
            in a location.
        """
        bg_color = button['bg']
        if bg_color == 'saddle brown':
            button.config(bg='white', activebackground='light grey')
        elif bg_color == 'white':
            button.config(bg='saddle brown', activebackground='light goldenrod')

    def read_env(self):
        """Reads the current state of the GUI and updates the environment variables"""
        for i, btn in enumerate(self.buttons):
            if i == 0:
                if btn['bg'] == 'white':
                    self.status[loc_A] = 'Clean'
                else:
                    self.status[loc_A] = 'Dirty'
            else:
                if btn['bg'] == 'white':
                    self.status[loc_B] = 'Clean'
                else:
                    self.status[loc_B] = 'Dirty'

    def update_env(self, agent):
        """
        Updates the GUI according to the agent's actions and current states.

        Parameters:
            agent (Agent): The vacuum agent.
        """
        self.read_env()
        # print(self.status)
        before_step = agent.location
        self.step()
        # print(self.status)
        # print(agent.location)
        move_agent(self, agent, before_step)
        #Updates the performance meter with the environment
        self.update_performance_title(agent)

    def create_performance_info(self):
        """Placeholder for additional performance functions."""
        pass


def create_agent(env, agent):
    """
    Creates the agent in the GUI and is kept independent of the environment.

    Parameters:
        env (Agent): The vacuum/GUI environment.
        agent (Agent): The vacuum agent.
    """
    env.add_thing(agent)
    # print(agent.location)
    if agent.location == (0, 0):
        env.agent_rect = env.canvas.create_rectangle(80, 100, 175, 180, fill='grey')
        env.text = env.canvas.create_text(128, 140, font="Helvetica 10 bold italic", text="Vacuum Agent")
    else:
        env.agent_rect = env.canvas.create_rectangle(200, 100, 295, 180, fill='grey')
        env.text = env.canvas.create_text(248, 140, font="Helvetica 10 bold italic", text="Vacuum Agent")


def move_agent(env, agent, before_step):
    """
    Moves the agent in the GUI when 'next' button is pressed.
    Parameters:
        env (Agent): The vacuum/GUI environment.
        agent (Agent): The vacuum agent.
        before_step (Callable): The agent's previous location before moving.

    """
    if agent.location == before_step:
        pass
    else:
        if agent.location == (1, 0):
            env.canvas.move(env.text, 120, 0)
            env.canvas.move(env.agent_rect, 120, 0)
        elif agent.location == (0, 0):
            env.canvas.move(env.text, -120, 0)
            env.canvas.move(env.agent_rect, -120, 0)


# TODO: Add more agents to the environment.
# TODO: Expand the environment to XYEnvironment.
if __name__ == "__main__":
    root = Tk()
    root.title("Vacuum Environment")
    root.geometry("420x380")
    root.resizable(0, 0)
    frame = Frame(root, bg='black')
    # reset_button = Button(frame, text='Reset', height=2, width=6, padx=2, pady=2, command=None)
    # reset_button.pack(side='left')
    next_button = Button(frame, text='Next', height=2, width=6, padx=2, pady=2)
    next_button.pack(side='left')
    frame.pack(side='bottom')
    env = Gui(root)
    agent = ReflexVacuumAgent()
    create_agent(env, agent)
    next_button.config(command=lambda: env.update_env(agent))
    root.mainloop()