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

    def handleAnswers(self, formAnswers):
        roundAnswers = []
        for i in range(5):
            givenAnswer = formAnswers[i]
            answerObject = Answer()
            answerObject.answer = givenAnswer
            if int(givenAnswer) == int(self.solutionColors[i]):
                answerObject.isCorrect = True
            else:
                answerObject.isCorrect = False
                answerObject = self.answerIsInSolution(answerObject)
            roundAnswers.append(answerObject)
        self.playerAnswers.append(roundAnswers)

    def answerIsInSolution(self, answerObject):
        for color in self.solutionColors:
            if (int(color) == int(answerObject.answer)):
                answerObject.inSolution = True
                break
            else:
                answerObject.inSolution = False
        return answerObject

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
        for x in range(4):
            foundColor = False
            while foundColor is False:
                posibleColor = random.randint(1, 5)
                for color in solutionColors:
                    if (posibleColor == color and self.doubleColors == False):
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
        session['playerAnswers'] = self.playerAnswersToJson()
        session['doubleColors'] = self.doubleColors

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
        db.execute("INSERT INTO players (name, number_of_tries) VALUES (?, ?)", (self.playerName, self.numberOfTries))

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
