from enum import Enum
from typing import List
from gameModel.block import Block

class Tile(Enum):
    VOID = 0
    GOAL = 1
    NORMAL = 2
    FRAGILE = 3
    SOFT_SWITCH = 4
    HEAVY_SWITCH = 5
    BRIDGE_ACTIVE = 6
    BRIDGE_CLOSE = 7


class Board:
    def __init__(self, rows: int, cols: int, initialTiles: List[List[Tile]] = None, 
                 startR: int = 0, startC: int = 0, isPermaToggle: bool = True):
        self.rows = rows
        self.cols = cols
        self.startR = startR
        self.startC = startC
        self.isPermaBridge = isPermaToggle # Whether when the bridge is toggled, it stays active permanently
        self.hasToggled = False
        self.isActiveBridge = False

        if initialTiles is not None:
            self.tiles = initialTiles
        # Initialize grid with NORMAL tiles if no initialTiles provided
        else:
            self.tiles = [[Tile.NORMAL for _ in range(cols)] for _ in range(rows)]

        self.initialTiles = [row[:] for row in self.tiles]

    def __repr__(self):
        return f"Board({self.rows}x{self.cols}, Start=({self.startR}, {self.startC}))"

    def copy(self) -> "Board":
        """Creates a deep copy of the board state for solver branch evaluation."""
        newBoard = Board.__new__(Board) # Bypasses __init__ setup

        # Deep copy the 2D grid matrix
        newBoard.tiles = [row[:] for row in self.tiles]
        
        # Note: if board tracks bridge states/switches, copy those attributes
        newBoard.isPermaBridge = self.isPermaBridge
        newBoard.hasToggled = self.hasToggled
        newBoard.isActiveBridge = self.isActiveBridge
        
        return newBoard

    def reset(self):
        """Restores grid back to its original layout."""
        # Deep copy initial_grid into current grid state
        self.tiles = [row[:] for row in self.initialTiles]

    def isInBounds(self, r: int, c: int) -> bool:
        """Helper to prevent out-of-bounds or negative indexing errors."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def getTile(self, r: int, c: int) -> Tile:
        """Return tile at row r and column c. Returns VOID tile if out of bounds."""
        if not self.isInBounds(r, c):
            return Tile.VOID
        return self.tiles[r][c]

    def setTile(self, r: int, c: int, tileType: Tile):
        """Set a single tile at (r, c)."""
        if self.isInBounds(r, c):
            self.tiles[r][c] = tileType

    def setRow(self, rowIndex: int, tileType: Tile):
        """Fill an entire row with a specific tile type."""
        if 0 <= rowIndex < self.rows:
            self.tiles[rowIndex] = [tileType] * self.cols

    def setColumn(self, colIndex: int, tileType: Tile):
        """Fill an entire column with a specific tile type."""
        if 0 <= colIndex < self.cols:
            for r in range(self.rows):
                self.tiles[r][colIndex] = tileType

    def getInvalidTiles(self) -> List[Tile]:
        """
        Returns a list of tiles that immdiately could results in game over
        """
        return [Tile.VOID, Tile.BRIDGE_CLOSE]

    def toggleBridges(self, ):
        """
        Activating any switch will results in enabling all bridge tiles
        """

        if (self.hasToggled): return

        self.isActiveBridge = not self.isActiveBridge
        targetTile = Tile.BRIDGE_ACTIVE if self.isActiveBridge else Tile.BRIDGE_CLOSE
        for r in self.tiles:
            if r == Tile.BRIDGE_ACTIVE or r == Tile.BRIDGE_CLOSE:
                r = targetTile

        if (self.isPermaBridge == True):
            self.hasToggled = True

    def breakFragile(self, r: int, c: int):
        if not self.isInBounds: return
        tile = self.tiles[r][c]
        if tile == Tile.FRAGILE:
            self.setTile(r, c, Tile.VOID)


    def specialInteractions(self, block: Block):
        """
        At the position of the block, process tile interactions, returns false when interaction results
        in the block position being at an invalid tile
        WARNING: this method skips Void tile
        Ex: switches and bridges 
        """
        occupiedTiles = [(block.r, block.c)]
        if block.dr == 1:
            occupiedTiles.append((block.r + 1, block.c))
        elif block.dc == 1:
            occupiedTiles.append((block.r, block.c + 1))

        toggled = False

        # Process tile interactions
        for r, c in occupiedTiles:
            tile = self.getTile(r, c)

            match tile:
                case Tile.FRAGILE:
                    if (block.isStanding()):
                        self.breakFragile(r, c)
                        return False

                case Tile.SOFT_SWITCH:
                    # Any block contact toggles soft switch
                    if not toggled:
                        self.toggleBridges()
                        toggled = True

                case Tile.HEAVY_SWITCH:
                    # Only toggles if the block is STANDING vertically on it
                    if block.isStanding() and not toggled:
                        self.toggleBridges()
                        toggled = True

        return True


    def resultingState(self, block: Block) -> "Board | None":
        """
        Returns a NEW Board instance representing the state after the block acts on tiles.
        Returns None if the block falls or collapses a fragile tile.
        To be used in solver
        """
        # Create a fresh clone so we don't mutate the current board
        nextBoard = self.copy()

        occupiedTiles = [(block.r, block.c)]
        if block.dr == 1:
            occupiedTiles.append((block.r + 1, block.c))
        elif block.dc == 1:
            occupiedTiles.append((block.r, block.c + 1))

        # Check if any part of the block is in the void
        for r, c in occupiedTiles:
            tile = nextBoard.getTile(r, c)
            isNotValid = not nextBoard.isInBounds(r, c) or tile == Tile.VOID or tile == Tile.BRIDGE_CLOSE
            if isNotValid:
                return None  # Invalid state (fell off)

        # Process tile interactions
        for r, c in occupiedTiles:
            tile = nextBoard.getTile(r, c)

            match tile:
                case Tile.FRAGILE:
                    # Fragile tiles only collapse when the block is STANDING
                    if block.isStanding():
                        nextBoard.setTile(r, c, Tile.VOID)
                        return None  # Block fell through fragile tile!

                case Tile.SOFT_SWITCH:
                    # Any block contact toggles/activates soft switch
                    nextBoard.toggleBridges()

                case Tile.HEAVY_SWITCH:
                    # Only toggles if the block is STANDING vertically on it
                    if block.isLying():
                        nextBoard.toggleBridges()

        return nextBoard
