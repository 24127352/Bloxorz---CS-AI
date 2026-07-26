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
    'B': Tile.BRIDGE_ACTIVE,
    'b': Tile.BRIDGE_CLOSE
}

def loadLevelFromJson(filePath: str) -> Tuple[Board, Block]:
    """Reads a JSON file and returns initialized (Board, Block) objects."""
    with open(filePath, 'r') as f:
        data = json.load(f)

    rows = data["rows"]
    cols = data["cols"]
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