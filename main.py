from levels.levelManager import LevelManager
from gameModel.gameController import GameController
from view import BloxorzView

def main():
    levelManager = LevelManager()
    board, block = levelManager.loadLevel()

    myGame = GameController(board, block)
    app = BloxorzView(myGame)

    # Make both use the same LevelManager
    app.levelManager = levelManager

    app.run()

if __name__ == "__main__":
    main()