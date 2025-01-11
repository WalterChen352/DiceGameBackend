import random

class Die:
    def __init__(self, faces):
        self.frozen=False
        self.faces=faces
        self.faceUpIndex=None
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
        return {'faces': result, 'faceIndex': self.faceUpIndex if self.faceUpIndex is not None else None }
    def info(self):
        return {'faces': self.toString(), 'faceIndex': self.faceUpIndex}
    def blank(self):
        self.faces[self.faceUpIndex]= BlankFace()

class HeartDie(Die):
    def __init__(self):
        super().__init__(heartDieFaces)

class MinusDie(Die):
    def __init__(self):
        super().__init__(minusDieFaces)

class PlusDie(Die):
    def __init__(self):
        super().__init__(plusDieFaces)

class Face:
    def __init__(self):
        return None
    def toString(self):
        return str(self.value)

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


class PowerFace(Face):
    def __init__(self):
        self.value=None

class PlusFace(PowerFace):
    def __init__(self):
        self.value="+"  

class MinusFace(PowerFace):
    def __init__(self):
        self.value="-"      

class BlankFace(Face):
    def __init__(self):
        self.value=''
    
heartDieFaces=[NumberFace(1), NumberFace(2), NumberFace(3), NumberFace(4), NumberFace(5), NumberFace(6)] 
plusDieFaces=[PlusFace(), PlusFace(), PlusFace(), PlusFace(),PlusFace(), PlusFace() ]
minusDieFaces=[MinusFace(), MinusFace(), MinusFace(), MinusFace(), MinusFace(), MinusFace()]