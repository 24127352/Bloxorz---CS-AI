from ursina import *

from gameModel.gameController import GameController
from gameModel.block import  Orientation, Direction
from gameModel.board import Tile
from inputHandler import InputHandler, Utility
from menu import StartMenu, PauseMenu


class BloxorzView:
    def __init__(self, gameModel: GameController):
        self.app = Ursina()
        self.gameModel = gameModel
        self.inputHandler = InputHandler()
        self.isPaused = False
        self.gameStarted = False

        # Set up camera view for an isometric perspective
        # camera.position = (5, 14, -10)
        # camera.rotation_x = 45

        # Visuals & Setup
        window.color = color.black50
        self.setupLighting()
        self.setupCamera()

        # Instantiate Menus
        self.startMenu = StartMenu(on_start_callback=self.startGame)
        self.pauseMenu = PauseMenu(
            on_resume_callback=self.resumeGame,
            on_restart_callback=self.restartLevel
        )

    def startGame(self):
        self.gameStarted = True
        self.tileColors = {
            Tile.NORMAL: color.light_gray,
            Tile.GOAL: color.magenta,
            Tile.FRAGILE: color.orange,
            Tile.SOFT_SWITCH: color.cyan,
            Tile.HEAVY_SWITCH: color.red,
            Tile.BRIDGE: color.brown
        }

        self.tileEntities = []
        self.renderBoard()

        # 3D Block mesh creation
        self.blockMesh = Entity(
            model='cube',
            color=color.orange,      # High-contrast color
            texture='white_cube',   # Sharpens edges
            origin_y=-0.5  # Pivot at the bottom face of the block
        )
        self.updateBlockMesh()

    def resumeGame(self):
        self.isPaused = False

    def restartLevel(self):
        """Resets the game model and refreshes 3D visual representations."""
        # 1. Reset model state
        self.gameModel.reset()

        self.renderBoard()

        # 3. Move 3D block back to start position and orientation
        self.blockMesh.rotation = (0, 0, 0)
        self.updateBlockMesh()

    def togglePause(self):
        if not self.gameStarted:
            return
        self.isPaused = not self.isPaused
        self.pauseMenu.toggle()

    def setupCamera(self):
        board = self.gameModel.board
        
        # 1. Calculate true center X and Z of the board grid
        centerX = (board.cols - 1) / 2.0
        centerZ = -(board.rows - 1) / 2.0
        
        # 2. Determine the bounding size of the stage
        maxDim = max(board.cols, board.rows)
        
        # 3. Scale distance dynamically:
        # - Height (Y) grows with grid size
        # - Pull back along Z into negative space relative to the bottom edge (-board.rows)
        heightY = maxDim * 1.35
        distanceZ = -board.rows - (maxDim * 0.75)
        
        camera.position = (centerX, heightY, distanceZ)
        
        # 4. Point directly at the board center
        camera.look_at(Vec3(centerX, 0, centerZ))

    def setupLighting(self):
        # Soft overall fill light so black shadows aren't pitch dark
        ambient = AmbientLight(color=color.rgba(100, 100, 100, 255))
        
        # Main sun light angled down to create clear top & side contrast
        sun = DirectionalLight(shadows=True)
        sun.look_at(Vec3(1, -2, -1))  # Angled light source
    
    def renderBoard(self):
        """Reads gameModel.board grid and spawns 3D floor tiles."""
        board = self.gameModel.board

        for r in range(board.rows):
            for c in range(board.cols):
                tileType = board.getTile(r, c)
                if tileType != Tile.VOID:
                    # c = X axis (columns), r = Z axis (rows)
                    tileEntity = Entity(
                        model='cube',
                        color=self.tileColors.get(tileType, color.white),
                        position=(c, -0.1, -r),
                        scale=(0.92, 0.2, 0.92),
                        texture='white_cube'      # Adds built-in subtle edge shadowing
                    )
                    self.tileEntities.append(tileEntity)

    def animateFall(self):
        """Animates the block tumbling down into the void."""
        fallDuration = 0.6
        
        # 1. Animate block dropping vertically on Y-axis
        targetY = self.blockMesh.y - 8
        self.blockMesh.animate_position(
            (self.blockMesh.x, targetY, self.blockMesh.z),
            duration=fallDuration,
            curve=curve.in_cubic
        )
        
        # 2. Add a slight tumbling rotation while falling
        self.blockMesh.animate_rotation(
            (self.blockMesh.rotation_x + 90, self.blockMesh.rotation_y, self.blockMesh.rotation_z + 45),
            duration=fallDuration,
            curve=curve.in_cubic
        )
    

    def updateBlockMesh(self):
        """
        Reads gameModel.block state and updates 3D mesh position and scale.
        Accounts for detaching roll math base positions.
        """
        currentBlock = self.gameModel.block
        r, c = currentBlock.r, currentBlock.c
        dr, dc = currentBlock.dr, currentBlock.dc
        targetScale = (0, 0, 0)
        targetPos = (0, 0, 0)

        if currentBlock.orientation == Orientation.STANDING:
            # Standing vertically: 1x2x1 scale, centered directly over tile (c, r)
            targetScale = (0.9, 1.8, 0.9)
            targetPos = (c, 0, -r)

        elif currentBlock.orientation == Orientation.LYING:
            if dc == 1:
                # Lying horizontally across columns c and c+1
                # Center point is c + 0.5 along X axis
                targetScale = (1.9, 0.9, 0.9)
                targetPos = (c + 0.5, 0, -r)

            elif dr == 1:
                # Lying vertically across rows r and r+1
                # Center point is r + 0.5 along Z axis
                targetScale = (0.9, 0.9, 1.9)
                targetPos = (c, 0, -(r + 0.5))

        # Apply scale 
        self.blockMesh.scale = targetScale
        self.blockMesh.position = targetPos

    def handleUrsinaInput(self, key: str):
        """Pass key to InputHandler, then update 3D mesh if state changed."""
        print(f"RAW KEY: '{key}'")

        uti = self.inputHandler.processKeyUtility(key)
        if uti is not None:
            match uti:
                case Utility.PAUSE: self.togglePause()
                case Utility.RESTART: self.restartLevel() # not complete yet
            return

        # 2. Block game inputs if game hasn't started or is paused
        if not self.gameStarted or self.isPaused:
            return

        dir = self.inputHandler.processKeyDirection(key)

        if dir is None:
            return

        self.gameModel.executeMove(dir)
        self.updateBlockMesh()

        if  self.gameModel.isGameOver or self.gameModel.hasWon:
            print ("Updating mesh")
            
            if self.gameModel.hasWon:
                print("Stage Complete!")


            elif self.gameModel.isGameOver:
                print("Game Over - Block fell into void!")
                self.animateFall()
                #self.restartLevel()

    def run(self):
        """Starts the main Ursina 3D render loop."""

        # Pass the function directly into Ursina's app instance
        self.app.input = self.handleUrsinaInput
        self.app.run()