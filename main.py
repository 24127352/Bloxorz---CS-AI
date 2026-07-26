from levels.levelLoader import loadLevelFromJson
from gameModel.gameController import GameController
from gameModel.state import State
from search.problem import Problem
from view import BloxorzView


def main():

    board, block = loadLevelFromJson("levels/level2.json")

    controller = GameController(board, block)

    problem = Problem(
        State(board, block)
    )

    app = BloxorzView(controller, problem)

    app.run()


if __name__ == "__main__":
    main()