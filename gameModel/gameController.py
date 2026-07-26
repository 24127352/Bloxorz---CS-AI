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
        self.block = Block(self.board.startR, self.board.startR, Orientation.STANDING)

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

        invalidTiles = self.board.getInvalidTiles()

        # 1. Validate ALL occupied tiles first before doing anything else
        for r, c in occupiedTiles:
            tile = self.board.getTile(r, c)
            if tile in invalidTiles:
                return False

            # Fragile tile check (standing upright on fragile = invalid)
            if tile == Tile.FRAGILE and block.isStanding():
                return False

        return True

    def isWinningState(self, block: Block = None) -> bool:
        """
        Winning condition: standing upright on the GOAL tile.
        If a Block instance is passed in, check winning condition for that block instead
        """
        if block is not None:
            return block.isStanding() and self.board.getTile(block.r, block.c) == Tile.GOAL
        
        if self.block.isStanding():
            return self.board.getTile(self.block.r, self.block.c) == Tile.GOAL
        
        return False

    def resultingState(self, dir: Direction) -> "GameController":
        """
        Attempts to move the block in a direction.
        Returns the state of the game
        """
        if self.isGameOver or self.hasWon:
            return None
        
        # Generate next state
        nextBlock = self.block.resultingState(dir)
        
        # Check if valid
        if not self.isValidBlockPosition(nextBlock):
            self.isGameOver = True
            return None

        nextBoard = self.board.resultingState()

        return GameController(nextBoard, nextBlock)

        
    def executeMove(self, dir: Direction) -> bool:
        """
        Attempts to move the block in a direction.
        Returns True if the move was valid and safe, False if the block fell/failed.
        """
        if self.isGameOver or self.hasWon:
            return False

        self.block.applyMove(dir)

        # Check if valid
        if not self.isValidBlockPosition(self.block):
            self.isGameOver = True
            return False

        # Check win condition
        if self.isWinningState():
            self.hasWon = True

        return True