from enum import Enum
from typing import List

class Tile(Enum):
    VOID = 0
    GOAL = 1
    NORMAL = 2
    FRAGILE = 3
    SOFT_SWITCH = 4
    HEAVY_SWITCH = 5
    BRIDGE = 6

#costs for each tile type, used in uniform cost search
TILE_COST = {

    Tile.NORMAL: 1,

    Tile.GOAL: 1,

    Tile.SOFT_SWITCH: 0.5,

    Tile.HEAVY_SWITCH: 0.5,

    Tile.BRIDGE: 1,

    Tile.FRAGILE: 5
}

#add switch toggles and bridge tiles to the board class, and add a method to toggle switches and bridges
class Board:
    def __init__(self, rows: int, cols: int, initialTiles: List[List[Tile]] = None,
                 startR: int = 0, startC: int = 0):
        self.rows = rows
        self.cols = cols
        self.startR = startR
        self.startC = startC
        self.bridgeMap = {}
        # Initialize grid with NORMAL tiles if no initialTiles provided
        if initialTiles is not None:
            self.tiles = initialTiles
        else:
            self.tiles = [[Tile.NORMAL for _ in range(cols)] for _ in range(rows)]

        self.initialTiles = [row[:] for row in self.tiles]

    def __repr__(self):
        return f"Board({self.rows}x{self.cols}, Start=({self.startR}, {self.startC}))"

    def reset(self):
        self.tiles = [row[:] for row in self.initialTiles]
        
    def isInBounds(self, r: int, c: int) -> bool:
        """Helper to prevent out-of-bounds or negative indexing errors."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def getTile(self, r: int, c: int) -> Tile:
        """Return tile at row r and column c. Returns VOID if out of bounds."""
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

    #function to add a bridge to the board, given the position of the switch and the position of the bridge
    def addBridge(self,
                switchPos,
                bridgePos):

        self.bridgeMap[switchPos] = bridgePos
    #function to toggle a bridge on the board, given the position of the switch
    def toggleBridge(self,
                    switchR,
                    switchC):

        key = (switchR, switchC)

        if key not in self.bridgeMap:
            return

        br, bc = self.bridgeMap[key]

        if self.tiles[br][bc] == Tile.BRIDGE:

            self.tiles[br][bc] = Tile.VOID

        else:

            self.tiles[br][bc] = Tile.BRIDGE