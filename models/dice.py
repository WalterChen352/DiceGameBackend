import random

class Die:
    def __init__(self, faces):
        self.frozen=False
        self.faces=faces
    def roll(self):
        if not self.frozen:
            self.faceUpIndex=random.randint(0, len(self.faces)-1)
        return
    def faceUp(self):
        return self.faces[self.faceUpIndex]
    def consume(self):
        self.faces[self.faceUpIndex]=BlankFace()
    def toString(self):
        result =[]
        for face in self.faces:
            result.append(face.toString())
        return {'faces': result, 'faceIndex': self.faceUpIndex }

class HeartDie(Die):
    def __init__(self):
        self.faces=heartDieFaces
        self.frozen=False
        

class Face:
    def __init__(self):
        return None

class NumberFace(Face):
    def __init__(self, val):
        self.value=val
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
    def toString(self):
        return str(self.value)

class PowerFace(Face):
    def __init__(self):
        return None

class BlankFace(Face):
    def __init__(self):
        return None
    def toString():
        return ''
    
heartDieFaces=[NumberFace(1), NumberFace(2), NumberFace(3), NumberFace(4), NumberFace(5), NumberFace(6)] 