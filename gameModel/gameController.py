from gameModel.block import *
from gameModel.board import *

class GameController:
    def __init__(self, board: Board, initialBlock: Block):
        self.board = board
        self.block = initialBlock
        self.isGameOver = False
        self.hasWon = False

    def reset(self):
        """Resets the game state and board back to level start."""
        # 1. Reset board tiles
        self.board.reset()

        # 2. Reset block state
        self.block = Block(self.board.startR, self.board.startC, orientation=Orientation.STANDING)

        # 3. Reset status flags & counters
        self.isGameOver = False
        self.hasWon = False

    def isValidBlockPosition(self, block: Block) -> bool:
        """
        Returns True if all tiles occupied by the block are safe.
        """
        # Determine all coordinates occupied by the block
        occupiedTiles = [(block.r, block.c)]
        if block.dr == 1:
            occupiedTiles.append((block.r + 1, block.c))
        elif block.dc == 1:
            occupiedTiles.append((block.r, block.c + 1))

        for r, c in occupiedTiles:
            tile = self.board.getTile(r, c)

            # 1. block falls into void/out of bounds
            if tile == Tile.VOID:
                return False

            # 2. Fragile tile collapses if block stands on it upright
            if tile == Tile.FRAGILE and block.orientation == Orientation.STANDING:
                return False

        return True

    def isWinningState(self) -> bool:
        """Winning condition: standing upright on the GOAL tile."""
        if self.block.orientation == Orientation.STANDING:
            return self.board.getTile(self.block.r, self.block.c) == Tile.GOAL
        return False

    def executeMove(self, dir: Direction) -> bool:
        """
        Attempts to move the block in a direction.
        Returns True if the move was valid and safe, False if the block fell/failed.
        """
        if self.isGameOver or self.hasWon:
            return False

        # Generate next state
        self.block = self.block.resultingState(dir)
        # Check for switch toggles
        tile = self.board.getTile(
            self.block.r,
            self.block.c
        )

        if tile == Tile.SOFT_SWITCH:

            self.board.toggleBridge(
                self.block.r,
                self.block.c
            )

        elif (
            tile == Tile.HEAVY_SWITCH
            and
            self.block.orientation == Orientation.STANDING
        ):

            self.board.toggleBridge(
                self.block.r,
                self.block.c
            )

        # Check if valid
        if not self.isValidBlockPosition(self.block):
            self.isGameOver = True
            return False

        # Check win condition
        if self.isWinningState():
            self.hasWon = True

        return True