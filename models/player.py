
from collections import Counter
from .dice import *


class Player:
    def __init__(self, startingLives, id):
        self.dice=[]
        self.lives=startingLives
        self.mostRecentBid=None
        self.uid = id
        for i in range (0, startingLives):
            self.dice.append(HeartDie())
    def lose(self, dieIndex):
        self.dice.pop(dieIndex)
    def add(self, die):
        self.dice.append(die)
    def rollAll(self):
        for die in self.dice:
            die.roll()
    def roll(self, dieIndex):
        self.dice[dieIndex].roll()
    def getRolls(self):
        rolls=[]
        dice=[]
        for die in self.dice:
            rolls.append(die.faces[die.faceUpIndex].value)
            dice.append(die.toString())
        count=Counter(rolls)
        return {
            'rolls': rolls,
            'count': count,
            'dice':dice
        }
    def postEffects(self):
        #TODO 
        return
    def preEffects(self):
        #TODO
        return
    def dieInfo(self):
        result=[]
        for die in self.dice:
            result.append(die.toString())
        return result
    def info(self):
        return {
            'dice': self.dieInfo(),
            'rolls': self.getRolls()
        }
    def cleanUp(self):
        for die in self.dice:
            die.faceUpIndex= None