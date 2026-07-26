from levels.levelManager import LevelManager
from gameModel.gameController import GameController
from gameModel.state import State
from gameModel.problem import Problem
from view import BloxorzView


def main():
    levelManager = LevelManager()
    board, block = levelManager.loadLevel()

    problem = Problem(State(board, block))

    myGame = GameController(board, block)
    app = BloxorzView(myGame, problem)

    # Make both use the same LevelManager
    app.levelManager = levelManager

    app.run()


if __name__ == "__main__":
    main()