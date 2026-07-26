from ursina import *

class StartMenu(Entity):
    def __init__(self, on_start_callback):
        super().__init__(parent=camera.ui)
        self.on_start_callback = on_start_callback

        # Background overlay
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.peach,
            scale=(2, 2),
            z=1
        )

        # Title Text
        self.title = Text(
            parent=self,
            text="BLOXORZ",
            origin=(0, 0),
            y=0.25,
            scale=10,
            color=color.azure
        )

        # Start Game Button
        self.start_button = Button(
            parent=self,
            text="Start Game",
            color=color.azure,
            highlight_color=color.olive,
            scale=(0.3, 0.08),
            y=0.0,
            on_click=self.start_game
        )

        # Quit Button
        self.quit_button = Button(
            parent=self,
            text="Quit",
            color=color.azure,
            highlight_color=color.olive,
            scale=(0.3, 0.08),
            y=-0.1,
            on_click=application.quit
        )

    def start_game(self):
        self.disable()  # Hide the start menu
        if self.on_start_callback:
            self.on_start_callback()

class PauseMenu(Entity):
    def __init__(self, on_resume_callback, on_restart_callback, on_next_level_callback, on_solver_callback):
        super().__init__(parent=camera.ui, enabled=False) # Start hidden
        self.on_resume_callback = on_resume_callback
        self.on_restart_callback = on_restart_callback
        self.on_next_level_callback = on_next_level_callback
        self.on_solver_callback = on_solver_callback

        # Dark overlay behind pause popup
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, 180),
            scale=(2, 2),
            z=1
        )

        # Pause Title
        self.title = Text(
            parent=self,
            text="GAME PAUSED",
            origin=(0, 0),
            y=0.2,
            scale=10,
            color=color.white50
        )

        # Resume Button
        self.resume_button = Button(
            parent=self,
            text="Resume",
            color=color.azure,
            scale=(0.3, 0.08),
            y=0.05,
            on_click=self.resume
        )

        # Restart Level Button
        self.restart_button = Button(
            parent=self,
            text="Restart Level",
            color=color.azure,
            scale=(0.3, 0.08),
            y=-0.06,
            on_click=self.restart
        )

        # Next level button
        self.next_level_button = Button(
            parent=self,
            text="Next Level",
            color=color.azure,
            scale=(0.3, 0.08),
            y = -0.17,
            on_click=self.nextLevel
        )

        # Solver button
        self.solver_button = Button(
            parent=self,
            text="Solver",
            color=color.azure,
            scale=(0.3,0.08),
            y=-0.28,
            on_click=self.solver
        )

        # Quit Button
        self.quit_button = Button(
            parent=self,
            text="Quit Game",
            color=color.olive,
            scale=(0.3, 0.08),
            y= -0.40,
            on_click=application.quit
        )

    def resume(self):
        self.disable()
        if self.on_resume_callback:
            self.on_resume_callback()

    def solver(self):
        self.disable()
        if self.on_solver_callback:
            self.on_solver_callback()


    def restart(self):
        self.disable()
        if self.on_restart_callback:
            self.on_restart_callback()

    def nextLevel(self):
        self.disable()
        if self.on_next_level_callback:
            self.on_next_level_callback()

    def toggle(self):
        self.enabled = not self.enabled

from ursina import Entity, Text, Button, color

class SolverMenu(Entity):
    def __init__(self, algorithms: list[str], on_select):
        """
        algorithms: A list of algorithm names, e.g. ["BFS", "DFS", "A* Search"]
        on_select: A callback function that takes the selected algorithm name as an argument.
                   e.g. def handleSelection(algo_name): ...
        """
        super().__init__(parent=camera.ui, enabled=False)

        self.algorithms = algorithms
        self.on_select = on_select
        self.elements = []

        self.create_menu()

    def create_menu(self):
        # 1. Background Panel
        num_buttons = max(len(self.algorithms), 1)
        panel_height = 0.15 + (num_buttons * 0.09)

        background = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(0.4, panel_height),
            position=(0, 0)
        )
        self.elements.append(background)

        # 2. Title
        title_y = (panel_height / 2) - 0.05
        title = Text(
            text="Solver",
            parent=self,
            position=(0, title_y),
            origin=(0, 0),
            scale=2,
            color=color.gold
        )
        self.elements.append(title)

        # 3. Algorithm Buttons
        start_y = title_y - 0.08
        spacing = 0.085

        for index, name in enumerate(self.algorithms):
            # Helper factory to capture 'name' properly and handle auto-hiding
            def make_handler(algo_name):
                def handler():
                    self.hide()  # Auto-hide menu on click
                    self.on_select(algo_name)  # Pass the chosen name out
                return handler

            btn = Button(
                text=name,
                parent=self,
                position=(0, start_y - (index * spacing)),
                scale=(0.3, 0.06),
                color=color.azure,
                highlight_color=color.cyan,
                on_click=make_handler(name)
            )
            self.elements.append(btn)

    def show(self):
        self.enabled = True

    def hide(self):
        self.enabled = False


        




