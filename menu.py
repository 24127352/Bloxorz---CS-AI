from ursina import *

class StartMenu(Entity):
    def __init__(self, on_start_callback, on_dfs_callback, on_ucs_callback):
        super().__init__(parent=camera.ui)
        self.on_start_callback = on_start_callback
        self.on_dfs_callback = on_dfs_callback
        self.on_ucs_callback = on_ucs_callback

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

        #dfs button

        self.dfs_button = Button(
            parent=self,
            text="Solve by DFS",
            scale=(0.3,0.08),
            y=-0.12,
            color=color.azure,
            on_click=self.solveDFS
        )
        #ucs button

        self.ucs_button = Button(
            parent=self,
            text="Solve by UCS",
            scale=(0.3,0.08),
            y=-0.24,
            color=color.azure,
            on_click=self.solveUCS
        )
        # Quit Button
        self.quit_button = Button(
            parent=self,
            text="Quit",
            color=color.azure,
            highlight_color=color.olive,
            scale=(0.3, 0.08),
            y=-0.36,
            on_click=application.quit
        )

    def start_game(self):
        self.disable()  # Hide the start menu
        if self.on_start_callback:
            self.on_start_callback()

    def solveDFS(self):
        self.disable()

        if self.on_dfs_callback:
            self.on_dfs_callback()


    def solveUCS(self):
        self.disable()

        if self.on_ucs_callback:
            self.on_ucs_callback()


class PauseMenu(Entity):
    def __init__(self, on_resume_callback, on_restart_callback):
        super().__init__(parent=camera.ui, enabled=False) # Start hidden
        self.on_resume_callback = on_resume_callback
        self.on_restart_callback = on_restart_callback

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

        # Quit Button
        self.quit_button = Button(
            parent=self,
            text="Quit Game",
            color=color.olive,
            scale=(0.3, 0.08),
            y=-0.17,
            on_click=application.quit
        )

    def resume(self):
        self.disable()
        if self.on_resume_callback:
            self.on_resume_callback()

    def restart(self):
        self.disable()
        if self.on_restart_callback:
            self.on_restart_callback()

    def toggle(self):
        self.enabled = not self.enabled