from flask import session
import random
from var_dump import var_dump

class Mastermind:

    def __init__(self):
        self.playerName = ""
        self.started = False
        self.gameFinisht = False
        self.doubleColors = False
        self.solutionColors = []
        self.playerAnswers = []

    def handleAnswers(self, formAnswers):
        roundAnswers = []
        for i in range(4):
            givenAnswer = formAnswers[i]
            answerObject = Answer()
            answerObject.answer = givenAnswer
            if givenAnswer == self.solutionColors[i]:
                answerObject.isCorrect = True
            else:
                answerObject.isCorrect = False
                answerObject = self.answerIsInSolution(answerObject)
            roundAnswers.append(answerObject)
        self.playerAnswers.append(roundAnswers)

    def answerIsInSolution(self, answerObject):
        for color in self.solutionColors:
            if (answerObject.isCorrect == False and color == answerObject.answer):
                answerObject.inSolution = True
                break
        return answerObject

    def isFinisht(self):
        lastRoundIndex = len(self.playerAnswers)
        givenAnswers = self.playerAnswers[lastRoundIndex];
        for answer in givenAnswers:
            if (answer.isCorrect == False):
                self.gameFinisht = False
                return self.gameFinisht
        self.gameFinisht = True
        return self.gameFinisht


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
        self.solutionColors = solutionColors

    def canPlay(self):
        return self.started

    def save(self):
        session['playerName'] = self.playerName
        session['doubleColors'] = self.doubleColors
        session['solutionColors'] = self.solutionColors
        session['gameFinisht'] = self.gameFinisht
        session['playerAnswers'] = self.playerAnswers

class Answer:

    def __init__(self):
        self.answer = ""
        self.isCorrect = False
        self.inSolution = True
