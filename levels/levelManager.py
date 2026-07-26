from levels.levelLoader import loadLevelFromJson


class LevelManager:

    def __init__(self):
        self.currentLevel = 1
        self.maxLevel = 12


    def loadLevel(self):
        path = f"levels/level{self.currentLevel}.json"

        return loadLevelFromJson(path)


    def nextLevel(self):

        if self.currentLevel < self.maxLevel:
            self.currentLevel += 1
            return self.loadLevel()

        print("All levels completed!")
        return None