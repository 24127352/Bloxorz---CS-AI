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


class Board:
    def __init__(self, rows: int, cols: int,
                 initialTiles: List[List[Tile]] = None,
                 startR: int = 0,
                 startC: int = 0):

        self.rows = rows
        self.cols = cols
        self.startR = startR
        self.startC = startC

        if initialTiles is None:
            self.tiles = [[Tile.NORMAL for _ in range(cols)] for _ in range(rows)]
        else:
            self.tiles = [row[:] for row in initialTiles]

        self.initialTiles = [row[:] for row in self.tiles]

        # Bridge system
        self.bridgeGroups = {}
        self.bridgeState = {}

    def __repr__(self):
        return f"Board({self.rows}x{self.cols})"

    def reset(self):
        self.tiles = [row[:] for row in self.initialTiles]

        for key in self.bridgeState:
            self.bridgeState[key] = True

    def isInBounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def getTile(self, r, c):
        if not self.isInBounds(r, c):
            return Tile.VOID

        return self.tiles[r][c]

    def setTile(self, r, c, tile):
        if self.isInBounds(r, c):
            self.tiles[r][c] = tile

    def setRow(self, rowIndex, tile):
        if 0 <= rowIndex < self.rows:
            self.tiles[rowIndex] = [tile] * self.cols

    def setColumn(self, colIndex, tile):
        if 0 <= colIndex < self.cols:
            for r in range(self.rows):
                self.tiles[r][colIndex] = tile

    # ============================
    # Bridge System
    # ============================

    def addBridge(self, switchPos, bridgeTiles):
        self.bridgeGroups[switchPos] = bridgeTiles
        self.bridgeState[switchPos] = True

    def toggleBridge(self, switchPos):

        if switchPos not in self.bridgeGroups:
            return

        self.bridgeState[switchPos] = not self.bridgeState[switchPos]

        newTile = (
            Tile.BRIDGE
            if self.bridgeState[switchPos]
            else Tile.VOID
        )

        for r, c in self.bridgeGroups[switchPos]:
            self.tiles[r][c] = newTile