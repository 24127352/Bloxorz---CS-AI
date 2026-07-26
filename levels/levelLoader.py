import json
from typing import Tuple
from gameModel.board import *
from gameModel.block import *

CHAR_TILE_MAP = {
    'X': Tile.VOID,
    '.': Tile.NORMAL,
    'F': Tile.FRAGILE,
    'G': Tile.GOAL,
    'S': Tile.NORMAL,  # Start tile sits on a normal floor tile
    'w': Tile.SOFT_SWITCH,
    'W': Tile.HEAVY_SWITCH,
    'B': Tile.BRIDGE
}


def loadLevelFromJson(filePath: str, isDebug: bool = True) -> Tuple[Board, Block]:
    """
    Reads a JSON file and returns initialized (Board, Block) objects.
    Set isDebug to false to turn off printing debug info
    """

    with open(filePath, 'r') as f:
        data = json.load(f)

    rows = data["rows"]
    cols = data["cols"]
    gridLines = data["grid"]

    # ===== DEBUG =====
    if (isDebug):
        print("\n========== LOADING LEVEL ==========")
        print(f"File: {filePath}")
        print(f"JSON rows: {rows}")
        print(f"JSON cols: {cols}")
        print(f"Grid rows: {len(gridLines)}")

        for i, row in enumerate(gridLines):
            print(f"Row {i}: length = {len(row)}")
        print("===================================\n")
    # =================

    # Convert character strings into a 2D matrix of Tile Enums
    tileMat = []

    for row_str in gridLines:
        row_tiles = [CHAR_TILE_MAP.get(char, Tile.VOID) for char in row_str]
        tileMat.append(row_tiles)

    # Instantiate Board
    board = Board(
        rows,
        cols,
        tileMat,
        data["start"]["r"],
        data["start"]["c"]
    )

    # ===== DEBUG =====
    if (isDebug):
        print("Board created successfully")
        print(f"Board.rows = {board.rows}")
        print(f"Board.cols = {board.cols}")
        print(f"Actual tile rows = {len(board.tiles)}")
        print(f"Actual first row length = {len(board.tiles[0])}")
        print("===============================\n")
    # =================

    # Read bridge definitions if they exist
    if "bridges" in data:
        for bridge in data["bridges"]:

            switchPos = tuple(bridge["switch"])

            tiles = [
                tuple(pos)
                for pos in bridge["tiles"]
            ]

            board.addBridge(
                switchPos,
                tiles
            )

    # Instantiate Starting Block
    block = Block(
        r=data["start"]["r"],
        c=data["start"]["c"],
        dr=0,
        dc=0,
        orientation=Orientation.STANDING
    )

    return board, block 