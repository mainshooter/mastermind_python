from flask import session
import random
from var_dump import var_dump
import sqlite3
import os

class Mastermind:

    def __init__(self):
        self.playerName = ""
        self.started = False
        self.gameFinisht = False
        self.doubleColors = False
        self.solutionColors = []
        self.playerAnswers = []
        self.numberOfTries = 0
        self.amountOfColors = 6
        self.amountOfPositions = 5

    def handleAnswers(self, formAnswers):
        for i in range(0, len(self.solutionColors)):
            self.solutionColors[i] = int(self.solutionColors[i])
        roundAnswers = []
        for i in range(self.amountOfPositions):
            givenAnswer = int(formAnswers[i])
            answerObject = Answer()
            answerObject.answer = givenAnswer
            roundAnswers.append(answerObject)

        for i in range(self.amountOfPositions):
            answerObject = roundAnswers[i]
            if answerObject.answer == self.solutionColors[i]:
                answerObject.isCorrect = True
            else:
                answerObject.isCorrect = False
                answerObject = self.answerIsInSolution(answerObject, roundAnswers)
        roundAnswers = self.answerColorIsCorrectEverywhere(roundAnswers)
        self.playerAnswers.append(roundAnswers)

    def answerIsInSolution(self, answerObject, roundAnswers):
        for color in self.solutionColors:
            if (color == answerObject.answer):
                answerObject.inSolution = True
                break
            else:
                answerObject.inSolution = False
        return answerObject

    def answerColorIsCorrectEverywhere(self, roundAnswers):
        solutionAnswers = self.solutionColors.copy()
        for i in range(0, len(self.solutionColors)):
            color = solutionAnswers[i]
            answerObject = roundAnswers[i]
            if (color == answerObject.answer):
                solutionAnswers[i] = None

        foundFromSolution = []
        for i in range(0, len(solutionAnswers)):
            answerObject = roundAnswers[i]
            if answerObject.isCorrect == True:
                continue

            alreadyHadSoMany = foundFromSolution.count(answerObject.answer)
            amountOfAnswerInSolution = solutionAnswers.count(answerObject.answer)
            if alreadyHadSoMany <= amountOfAnswerInSolution and amountOfAnswerInSolution > 0:
                pass
            else:
                answerObject.inSolution = False
            foundFromSolution.append(answerObject.answer)

        return roundAnswers

    def isFinisht(self):
        self.numberOfTries = self.numberOfTries + 1
        lastRoundIndex = len(self.playerAnswers) - 1
        givenAnswers = self.playerAnswers[lastRoundIndex];
        for answer in givenAnswers:
            if (answer.isCorrect == False):
                self.gameFinisht = False
                return self.gameFinisht
        self.gameFinisht = True
        return self.gameFinisht


    def generate(self):
        solutionColors = []
        for x in range(0, self.amountOfPositions):
            foundColor = False
            while foundColor is False:
                posibleColor = random.randint(1, self.amountOfColors)
                for color in solutionColors:
                    if (posibleColor == color and self.doubleColors == False):
                        foundColor = False
                        break
                    else:
                        foundColor = True
                if foundColor is True or len(solutionColors) == 0:
                    solutionColors.append(posibleColor)
                    break
        self.solutionColors = solutionColors

    def canPlay(self):
        return self.started

    def save(self):
        session['playerName'] = self.playerName
        session['doubleColors'] = self.doubleColors
        session['solutionColors'] = self.solutionColors
        session['gameFinisht'] = self.gameFinisht
        session['playerAnswers'] = self.playerAnswersToJson()
        session['doubleColors'] = self.doubleColors
        session['amountOfPositions'] = self.amountOfPositions

    def playerAnswerJsonToObject(self, playerAnswers):
        self.playerAnswers = []
        for round in playerAnswers:
            roundAnswers = []
            for answer in round:
                answerObject = Answer()
                answerObject.answer = answer["answer"]
                answerObject.isCorrect = answer["isCorrect"]
                answerObject.inSolution = answer["inSolution"]
                roundAnswers.append(answerObject)
            self.playerAnswers.append(roundAnswers)
        pass

    def playerAnswersToJson(self):
        returnResult = []
        for round in self.playerAnswers:
            roundAnswers = []
            for answer in round:
                roundAnswers.append(answer.serialize())
            returnResult.append(roundAnswers)
        return returnResult

    def saveToDb(self):
        db = Database()
        db.execute("INSERT INTO players (name, number_of_tries, `date`) VALUES (?, ?, DATE('now'))", (self.playerName, self.numberOfTries))

class Answer:

    def __init__(self):
        self.answer = ""
        self.isCorrect = False
        self.inSolution = False

    def serialize(self):
        return {
            "answer": self.answer,
            "isCorrect": self.isCorrect,
            "inSolution": self.inSolution,
        };

class Database:

    def __init__(self):
        self.openDb()

    def openDb(self):
        self.db = sqlite3.connect('database.db')

    def execute(self, query, bindings):
        self.openDb()
        cur = self.db.cursor()
        cur.execute(query, bindings)
        self.db.commit()
        self.close();

    def query(self, query, bindings=None):
        self.openDb()
        curs = self.db.cursor()
        if bindings:
            curs.execute(query, bindings)
        else:
            curs.execute(query)

        while True:
            row = curs.fetchone()
            if not row:
                return None
            yield row
        self.close()

    def close(self):
        self.db.close()
