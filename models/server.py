import random
import string

def generateRoomCode():
    N = 5
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
    print(res)
    return res



    





