import json
from typing import Tuple
from gameModel.board import *
from gameModel.block import *

CHAR_TILE_MAP = {
    'X': Tile.VOID,
    '.': Tile.NORMAL,
    'F': Tile.FRAGILE,
    'G': Tile.GOAL,
<<<<<<< HEAD
    'S': Tile.NORMAL,
=======
    'S': Tile.NORMAL,  # Start tile sits on a normal floor tile
>>>>>>> d766cf41537dc9cf449b55cf049a2b3df4c6dade
    'w': Tile.SOFT_SWITCH,
    'W': Tile.HEAVY_SWITCH,
    'B': Tile.BRIDGE
}

<<<<<<< HEAD

def loadLevelFromJson(filePath: str) -> Tuple[Board, Block]:

    with open(filePath, "r") as f:
=======
def loadLevelFromJson(filePath: str) -> Tuple[Board, Block]:
    """Reads a JSON file and returns initialized (Board, Block) objects."""
    with open(filePath, 'r') as f:
>>>>>>> d766cf41537dc9cf449b55cf049a2b3df4c6dade
        data = json.load(f)

    rows = data["rows"]
    cols = data["cols"]
<<<<<<< HEAD

    tileMat = []

    for row in data["grid"]:
        tileMat.append(
            [CHAR_TILE_MAP.get(ch, Tile.VOID) for ch in row]
        )

    board = Board(
        rows,
        cols,
        tileMat,
        data["start"]["r"],
        data["start"]["c"]
    )

    # ---------------------------------------------------
    # NEW
    # Read bridge definitions if they exist
    # ---------------------------------------------------

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

    # ---------------------------------------------------

    block = Block(
        r=data["start"]["r"],
        c=data["start"]["c"],
        dr=0,
        dc=0,
        orientation=Orientation.STANDING
    )

    return board, block
=======
    gridLines = data["grid"]

    # Convert character strings into a 2D matrix of Tile Enums
    tileMat = []
    for row_str in gridLines:
        row_tiles = [CHAR_TILE_MAP.get(char, Tile.VOID) for char in row_str]
        tileMat.append(row_tiles)

    # Instantiate Board
    levelBoard = Board(
        rows=rows, 
        cols=cols, 
        initialTiles=tileMat,
        startR=data["start"]["r"], 
        startC=data["start"]["c"]
    )

    # Instantiate Starting Block (Standing vertically at start position)
    initialBlock = Block(
        r=data["start"]["r"], 
        c=data["start"]["c"], 
        dr=0, 
        dc=0, 
        orientation=Orientation.STANDING
    )

    return levelBoard, initialBlock
>>>>>>> d766cf41537dc9cf449b55cf049a2b3df4c6dade
