import json
from typing import Tuple
from gameModel.board import *
from gameModel.block import *

CHAR_TILE_MAP = {
    'X': Tile.VOID,
    '.': Tile.NORMAL,
    'F': Tile.FRAGILE,
    'G': Tile.GOAL,
    'S': Tile.NORMAL,
    'w': Tile.SOFT_SWITCH,
    'W': Tile.HEAVY_SWITCH,
    'B': Tile.BRIDGE
}


def loadLevelFromJson(filePath: str) -> Tuple[Board, Block]:

    with open(filePath, "r") as f:
        data = json.load(f)

    rows = data["rows"]
    cols = data["cols"]

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