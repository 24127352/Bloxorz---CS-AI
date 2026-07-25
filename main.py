from levels.levelLoader import loadLevelFromJson
from gameModel.gameController import GameController
from view import BloxorzView

def main():
    board, block = loadLevelFromJson("levels/level2.json")
    myGame = GameController(board, block)
    app = BloxorzView(myGame)
    app.run()

if __name__ == "__main__":
    main()