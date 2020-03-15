from flask import session
import random
from var_dump import var_dump

class Mastermind:

    def __init__(self):
        self.playerName = ""
        self.started = False
        self.doubleColors = False
        pass

    def generate(self):
        solutionColors = []
        for x in range(4):
            foundColor = False
            while foundColor is False:
                posibleColor = random.randint(1, 5)
                for color in solutionColors:
                    if (posibleColor == color):
                        foundColor = False
                        break
                    else:
                        foundColor = True
                if foundColor is True or len(solutionColors) == 0:
                    solutionColors.append(posibleColor)
        var_dump(solutionColors)


    def save(self):
        session['playerName'] = self.playerName
        session['doubleColors'] = self.doubleColors
