import random
from enum import Enum
from typing import Callable

def increment(face):
    face.value= face.value+1

def freeze(die):
    die.frozen=True

def decrement(face):
    face.value=face.value-1

def reroll(die):
    die.roll()

class Die:
    def __init__(self, faces, name):
        self.frozen=False
        self.faces=faces
        self.faceUpIndex=None
        self.name =name
    def roll(self):
        if not self.frozen:
            self.faceUpIndex=random.randint(0, len(self.faces)-1)
        else:
            self.frozen=False
        return
    def faceUp(self):
        #print(f'{self.name} has faceUp of {self.faceUpIndex}')
        return self.faces[self.faceUpIndex]
    def consume(self):
        self.faces[self.faceUpIndex]=BlankFace()
    def toString(self):
        result =[]
        for face in self.faces:
            result.append(face.toString())
        return {'faces': result, 'faceIndex': self.faceUpIndex if self.faceUpIndex is not None else None }
    def info(self):
        return {'faces': self.toString(), 'faceIndex': self.faceUpIndex}
    def blank(self):
        self.faces[self.faceUpIndex]= BlankFace()

class HeartDie(Die):
    def __init__(self):
        super().__init__(heartDieFaces, "Heart Die")

class MinusDie(Die):
    def __init__(self):
        super().__init__(minusDieFaces, "Minus Die")

class PlusDie(Die):
    def __init__(self):
        super().__init__(plusDieFaces, "Plus Die")

class FreezeDie(Die):
    def __init__(self):
        super().__init__(freezeDieFaces, "Freeze Die")

class Face:
    def __init__(self, value):
        self.value=value
    def toString(self):
        return {
         'value':   str(self.value),
         'type': self.type

        }
class NumberFace(Face):
    def __init__(self, val):
        self.value=val
        self.type='number'
    def value(self):
        return self.value
    def increment(self):
        self.value+=1
    def decrement(self):
        self.value-=1
    def add(self, val):
        self.value+=val
    def set(self, val):
        self.value=val

class Timing(Enum):
    PRE= 1
    BID = 2
    POST = 3

class PowerFace(Face):
    def __init__(self, value:str, t:Timing, c:bool, f:Callable, targetType:str):
        super().__init__(value)
        self.type='power'
        self.timing = t
        self.consume = c
        self.power = f
        self.targetType = targetType
        self.target= None
    def usePower(self):
        self.power(self.target)
    def setTarget(self, target):
        self.target=target
    def prompt(self):
        return self.prompt.toDict()

class PlusFace(PowerFace):
    def __init__(self):
        super().__init__("+", Timing.POST, True,increment, "Face") 
        self.prompt= Prompt('Choose a face to increment', 'face', 0, 1, faceType='number') 

class MinusFace(PowerFace):
    def __init__(self):
        super().__init__("-", Timing.POST, True,decrement, "Face")
        self.prompt= Prompt('Choose a face to decrement', 'face', 0, 1, faceType='number')

class FreezeFace(PowerFace):
    def __init__(self):
        super().__init__("F", Timing.POST, True,freeze, "Die")
        self.prompt= Prompt('Choose a face to freeze', 'die', 0, 1)     

class RerollFace(PowerFace):
    def __init__(self):
        super().__init__("R", Timing.PRE, True, reroll, "Die")

class BlankFace(PowerFace):
    def __init__(self):
        super().__init__("") 
    
class Prompt:
    def __init__(self, prompt, targetType, minSelections, maxSelections, dieType='', faceType=''):
        self.prompt=prompt
        self.targetType=targetType
        self.minSelections=minSelections
        self.maxSelections=maxSelections
        self.dieType=dieType
        self.faceType=faceType
    def toDict(self):
        return {
            'prompt': self.prompt,
            'minSelections': self.minSelections,
            'maxSelections': self.maxSelections,
            'targetType': self.targetType,
            'dieType': self.dieType,
            'faceType': self.faceType
        }

heartDieFaces=[NumberFace(1), NumberFace(2), NumberFace(3), NumberFace(4), NumberFace(5), NumberFace(6)] 
plusDieFaces=[PlusFace(), PlusFace(), PlusFace(), PlusFace(),PlusFace(), PlusFace() ]
minusDieFaces=[MinusFace(), MinusFace(), MinusFace(), MinusFace(), MinusFace(), MinusFace()]
freezeDieFaces=[FreezeFace(),FreezeFace(),FreezeFace(),FreezeFace(),FreezeFace(),FreezeFace()]

