import random
import re
import sys
from collections import Counter

class Die:
    def __init__(self, faces, type):
        self.faces=faces
        self.type=type
        self.faceUp=None
        self.freeze=False
    
    def roll(self):
        if self.freeze:
            self.freeze=False
            return
        self.faceUp=random.randint(0, len(self.faces)-1)
    def displayRoll(self):
        roll=None
        if self.faceUp is None or self.faceUp>= len(self.faces):
            roll=None
        else:
            roll=self.faces[self.faceUp]
        frozen=""
        if self.freeze:
            frozen =colors.CYAN+" [Frozen]"+colors.RESET
        print(f"{self.type}: [{checkColor(self)+str(roll)+colors.RESET}]{frozen}")
    def update(self, index, new):
        self.faces[index]=new
    def add(self, newFace):
        self.faces.append(newFace)



class colors:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


def checkColor(die):
    match die.type:
        case _:
            if die.faceUp is None:
                return ""
            return checkFaceColor(die.faces[die.faceUp])

nums=r'[0-9]+'
negNums=r'-[0-9]+'
preEffects=r'[ASR]'
bidEffects=r'[~$P]'
afterEffects=r'[BEFX!@=+-]'

def checkFaceColor(face):
    if face is None:
        return colors.RESET

    if re.search(negNums, face):
        return colors.RED
    if re.search(nums, face):
        return colors.GREEN
    if re.search(bidEffects, face):
        return colors.YELLOW
    if re.search(preEffects, face):
        return colors.MAGENTA
    if re.search(afterEffects, face):
        return colors.BLUE
    return colors.RESET

def heartDie():
    return [Die(["1","2","3","4","5","6"],
                "❤️  Die")]

def plusDie():
    return [Die(["+", "+", "+","+","+", "+"], "Plus Die")]

def minusDie():
    return [Die(["-", "-", "-", "-", "-", "-"], "Minus Die")]

def rerollDie():
    return [Die(["R", "R", "R", "R"], "Reroll Die")]

def shapeshifterDie():
    return [Die(["X"], "Shapeshifter Die")]

def passDie():
    return [Die(["P", "P", "P", " ", " ", " "], "Pass Die")]

def cowardsDie():
    return [Die(["~", "~", "~", "~", " ", " "], "Coward's Die")]

def addBlankDie():
    return [Die(["B", "B", "B", "B", "B", "B"], "Blank Die")]

def cloneFaceDie():
    return [Die(["=", "=", "=", "=", "=", "="], "Clone Face Die")]

def snakeEyes():
    return [Die(["1", "1", "1", " ", " ", " "], "Snake Eyes Die"), Die(["1", "1", "1", " ", " ", " "], "Snake Eyes Die")]

def splitDice():
    return [Die(["1","2","3"], "Split Die"), Die(["4","5","6"], "Split Die")]

def faceStealDie():
    return [Die(["X", "X", "X", "X", "X", "X"], "Face Steal Die")]

# def contagionDie():
#     return [Die(["!", " ", " ", " ", " ", " ", " ", " "], "Contagion Die")]

def wagerDie():
    return [Die(["$" ," ", " "], "Wager Die")]

def advantageDie():
    return [Die(["A", "A", "A", "A"], "Advantage Die")]

def evilDice():
    return [Die(["-1", "-2", "-3", "-4", "-5", "-6"], "Evil Die"),Die(["-1", "-2", "-3", "-4", "-5", "-6"], "Evil Die") ]

def spyDie():
    return [Die(["S", "S", "S", "S"], "Spy Die")]

def swapDie():
    return [Die(["@", "@", "@", "@", "@", "@", " ", " "], "Swap Die")]

def wildDie():
    return [Die(["1", "2", "3", "4", "5", "6", " ", " ", " ", " ", " ", " "], "Wild Die")]

def d3s():
    return [Die(["2", "3", "4"], "D3"), Die(["2", "3", "4"], "D3")]

def d6():
    return [Die(["1", "2", "3", "4", "5", "6"], "D6")]

def pairedDie():
    return [Die(["1", "2", "3", "4", "5", "6"],"Paired Die"),Die(["1", "2", "3", "4", "5", "6"],"Paired Die") ]

def echoDie():
    return [Die (["E", "E", "E", "E", "E", "E"], "Echo Die")]

def freezeDie():
    return [Die (["F", "F", "F", "F", "F", "f"], "Freeze Die")]

DICE=[heartDie(), plusDie(), minusDie(), rerollDie(), spyDie(), d6(), advantageDie(), wagerDie(), snakeEyes(), passDie(), addBlankDie(), evilDice(), faceStealDie(), splitDice(), d3s(), cowardsDie(), pairedDie(), freezeDie(), echoDie()]


class LiarsDie(Die):
    def __init__(self):
        self.faces=[]
        self.type="Liar's Die"
        self.tempType=""
        self.faceUp=None
        self.freeze=False
    def roll(self):
        if self.freeze:
            self.freeze=False
            return
        dieIndex=DICE[random.randint(0, len(DICE)-1)]
        die=dieIndex[random.randint(0,len(dieIndex)-1)]
        die.roll()
        self.faceUp=die.faceUp
        self.tempType=die.type
    def displayRoll(self):
        print (f"{self.type}: [{checkColor(self)+str(die.faces[self.faceUp])+colors.RESET}] on a {self.tempType}")



def rollAll(dice):
    result=[]
    for die in dice:
        die.roll()
        die.displayRoll()
        if die.faceUp is not None:
            result.append(str(die.faces[die.faceUp]))
    summary=Counter(result)
    sortedSummary=sorted(summary.keys())
    for roll in sortedSummary:
        print(f"{checkFaceColor(roll)+roll+colors.RESET}'s: {summary[roll]} ")

def showRolls(dice):
    for die in dice:
        die.displayRoll()

def displayDice(dice):
    result=[]
    for index, die in enumerate(dice):
        print(f"Die {index+1}  ({die.type}): ", end='')
        for face in die.faces:
            print(f"[{checkFaceColor(face)+face+colors.RESET}]", end='')
        roll="None"
        if die.faceUp is not None:
            roll=die.faces[die.faceUp]
        frozen=""
        if die.freeze:
            frozen =colors.CYAN+" [Frozen]"+colors.RESET
        print(f" Roll: [{checkColor(die)+roll+colors.RESET}]{frozen}\n")
        result.append(roll)
    summary=Counter(result)
    summary = {key: value for key, value in summary.items() if key is not None}
    sortedSummary=sorted(summary.keys())
    for roll in sortedSummary:
        print(f"{checkFaceColor(roll)+roll+colors.RESET}'s: {summary[roll]} ")
     


def displayFaces(die):
    for index, face in enumerate(die.faces):
        print(f"Face {index+1}: [{face}]")


def editDie(dice):
    displayDice(dice)
    die=getUserInt("Enter the number for the die you would like to edit: ", 1, len(dice)+1)
    if die is False:
        return
    die=dice[die-1]
    face=None
    edit=None
    while edit is None:
        prompt=input("Would you like to edit a face or add faces? ").lower()
        match prompt:
            case "edit" | "Edit" | "e" | "E":
               edit=True
            case "add" |"Add"|"a"|"A":
               edit=False
            case "cancel"|"q"|"quit":
                return
    val=None
    if edit:
        displayFaces(die)
        face=getUserInt("Select the face you would like to edit: ", 1, len(die.faces)+1)
        if face is False:
            return
        while True :
            val=input("Give new value of face (underscore will be converted to blank): ")
            if val=='q' or val =='quit' or val=='cancel':
                return
            elif len(val) <=0:
                print("Error: face must be at least single character")
                break
            else:
                break
        if val=="_":
            val=" "
        die.update(face-1, val)
    else:
        while True :
            val=input("Give values of new faces delimited by spaces with underscore as blanks. For example: 1 2 3 4 5 6 _ \n ")
            if val=='q' or val =='quit' or val=='cancel':
                return
            else:
                faces = [elem.strip() for elem in val.split(" ") if elem.strip()]
                for face in faces:
                    if face =='_':
                        face= ' '
                break
        die.faces+=faces
    displayDice(dice)


def customDie(dice):
    die = input("Input the faces of the die delimited by spaces and a blank as an underscore. For example: 1 2 3 4 5 6 _ \n")
    faces = [elem.strip() for elem in die.split(" ") if elem.strip()]
    for face in faces:
        if face =='_':
            face= ' '
    type= input("Optional: enter the type of you die. Will be custom by default \n")
    if type=="":
        type="Custom"
    dice.append(Die(faces, type))


    


def addDie(dice):
    die=input("Which die/dice would you like to add? \n" ).lower()
    new=None
    match die:
        case "heart" | "heart die" | "heartdie":
            new=heartDie()
        case "plus" | "plus die":
            new=plusDie()
        case "minus" | "minus die":
            new=minusDie()
        case "reroll" | "reroll die":
            new=rerollDie()
        case "pass" | "pass die":
            new=passDie()
        case "add blank" | "add blank die":
            new=addBlankDie()
        case "clone face"| "clone face die":
            new=cloneFaceDie()
        case "snake eyes"| "snake":
            new=snakeEyes()
        case "split dice"|"split"|"split die":
            new=splitDice()
        # case "contagion"|"contagion die":
        #     new=contagionDie()
        case "wager"|"wager die":
            new=wagerDie()
        case "advantage"|"advantage die":
            new=advantageDie()
        case "evil"| "evil dice"|"evil die":
            new=evilDice()
        case "spy"|"spy die":
            new=spyDie()
        case "swap"|"swap die":
            new=swapDie()
        case "wild"| "wild die":
            new=wildDie()
        case "d3":
            new=d3s()
        case "d6":
            new=d6()
        case "pair"|"paired"|"paired dice":
            new=pairedDie()
        case "liar"|"liar's die"|"liars die":
            new=[LiarsDie()]
        case "coward"|"cowards"|"coward's"|"cowards die"|"coward's die":
            new=cowardsDie()
        case "shapeshifter"|"shapeshifter die":
            new=shapeshifterDie()
        case "face steal"|"face steal die":
            new=faceStealDie()
        case "freeze"|"freeze die":
            new=freezeDie()
        case "echo"|"echo die":
            new=echoDie()
        case "custom":
            customDie(dice)
        case "cancel"|"quit"|"q":
            return
    if new is not None:
        dice.extend(new)
    else:
        print("Dice not found. Returning to main menu.")
    displayDice(dice)

def removeDie(dice):
    displayDice(dice)
    dieIndex=getUserInt("Select which die to remove: ", 1, len(dice)+1)
    if dieIndex is not False:
        dice.pop(dieIndex-1)
    lives=0
    for die in dice:
        if die.type =="❤️  Die":
            lives+=1
    return lives

def freeze(dice):
    displayDice(dice)
    dieIndex=getUserInt("Select which die to freeze: \n", 1, len(dice)+1)-1
    dice[dieIndex].freeze=True

def reroll(dice):
    for index, die in enumerate(dice):
        print(f"{index+1 } ", end='')
        die.displayRoll()
    dieIndex= getUserInt("Please select which die to reroll: ", 1, len(dice)+1)
    if dieIndex is False:
        return
    dice[dieIndex-1].roll()
    for die in dice:
        die.displayRoll()


# def blankRandom(dice):
#     die_index=random.randint(0, len(dice)-1)
#     dice[die_index].faceUp=" "
#     showRolls(dice)

def getUserInt(prompt, lowerBound, upperBound):
    msg=None
    while True:
        try:
            msg=input(prompt)
            result= int(msg)
            if result not in range (lowerBound, upperBound):
                print(f"Error: please provide a number between {lowerBound} and {upperBound-1}")
                continue
            return result
        except ValueError:
            if msg =='q' or msg== 'quit' or msg=='cancel':
                return False
            print("Error: please provide a number")

def randomSelect(dice):
    dieIndex=random.randint(0, len(dice)-1)
    dice[dieIndex].displayRoll()

def advantage(dice):
    for index, die in enumerate(dice):
        print(f"{index+1 } ", end='')
        die.displayRoll()
    dieIndex= getUserInt("Please select which die to roll with advantage: ", 1, len(dice)+1)
    if dieIndex is False:
        return
    dieIndex=dieIndex-1
    die=die[dieIndex]
    oldIndex=die.faceUp
    oldVal=die.faces[die.faceUp]
    die.roll()
    newVal=die.faces[die.faceUp]
    while True:
        choice=input(f"Your old roll was [{oldVal}]. Your new roll is [{newVal}]. Keep new roll? (y/n) ").lower()
        match choice:
            case "q"|"quit"|"no"|"n":
                die.faceUp=oldIndex
                return
            case "yes"| "y":
                return


# def setRoll(dice):
#     displayDice(dice)
#     dieIndex=getUserInt("Please select which die's roll you would like to set : " ,1, len(dice)+1)
#     if dieIndex is False:
#         return
#     dieIndex=dieIndex-1
#     roll=input("What would you like to change the roll to? ")
#     dice[dieIndex].faceUp=roll    

def helpMessage():
    print("Here are the following commands for the interface:")
    print(colors.GREEN+"-rules: rules explanation"+colors.RESET)
    print(colors.RED+"-r/roll: roll all dice"+colors.RESET)
    print("-e/edit: edit the faces or add new face to dice")
    print("-a/add: add batches of dice or custom dice to your dice pool. Enter 'custom' for custom dice")
    print("-d/display: show all faces of your dice")
    print("-l/lose: remove a die fro your dice pool")
    print("-reroll: reroll a single die")
    print("-b/blank: blanks a single die")
    print("-random: select a random die from your pool and display its current roll")
    print("-adv/advan/advantage: reroll a die of your choice with advantage")
    print("-set/setroll: set the roll of one of your dice to a value")
    print("Additionally, enter q, quit, or cancel at anytime to exit a command")


def rules():
    print("Welcome to Deceiver's Dice!")
    print("The objective of the game is to bluff and deceive your way until you are the last deceiver standing.\n")

    print("Round Overview:")
    print(f"\t{colors.GREEN}1) Roll dice{colors.RESET}")
    print("\t\tAll players roll all of their dice secretly.")
    print(f"\t{colors.MAGENTA}2) Resolve pre-bid effects{colors.RESET}")
    print("\t\tIn reverse bidding order, players resolve their pre-bid effects.")
    print(f"\t{colors.YELLOW}3) Bidding{colors.RESET}")
    print(f"\t\tThe starting player leads with a bid, and each player after that can raise or challenge the previous bid. A challenge ends bidding for the round.")
    print(f"\t\tA bid consists of two parts: quantity and face. The face must be a number.")
    print(f"\t\tA bid is a wager of at least how many faces of the type have been rolled by all players.")
    print("\t\tExample: \"3 3's\" is equivalent to stating \"Between all players, I believe there are at least 3 3's\".")
    print("\t\tBy default, 1's rolled are wild and can count towards any bid.\n")
    print("\t\tA raise must do one of the following:")
    print("\t\t\t-Maintain the quantity and raise the face of the previous bid.")
    print("\t\t\t-Raise the quantity of the previous bid. The face can be maintained or changed to a higher or lower value.")
    print("\t\tThe following are legal raises to 3 3's:")
    print("\t\t\t3 4's")
    print("\t\t\t4 2's")
    print("\t\t\t4 4's")
    print("\t\tThe following are illegal raises to 3 3's:")
    print("\t\t\t3 2's")
    print("\t\t\t2 4's")
    print("\t\t\t3 3's\n")

    print("\t\tOnce a challenge is issued, starting from the bidder and in bidding order, players resolve their bid effects.")
    print("\t\tCount up the relevant face and wilds to get the total for the round.")
    print("\t\tIf the bidder's quantity is less than or equal to the total, the bidder wins. Otherwise, the challenger wins.")
    print("\t\tThe loser of the challenge loses a heart die of their choice and becomes the starting player. If that player has no more remaining heart dice they are eliminated.")

    print(f"\t{colors.BLUE}4)Resolve post-bid effects{colors.RESET}")
    print(f"\t\tPlayers resolve their post-bid effects in bidding order starting from the new starting player (loser of the challenge).")


    print("The last player remaining is the winner! Best of luck scheming and bluffing your way to victory.")

    print("\n")

def abilities():
    print()

def consume(dice):
    displayDice(dice)
    dieIndex=getUserInt("Select which die you would like to consume: \n",1, len(dice)+1)-1
    if dieIndex is False:
        return
    displayFaces(dice[dieIndex])
    face=getUserInt("Select which face you would like to consume: \n",1, len(dice[dieIndex].faces)+1)-1
    if face is False:
        return
    dice[dieIndex].faces[face]=' '

def main():
    lives=getUserInt("Number of starting heart dice: ", 1, sys.maxsize)
    if lives is False:
        print("Come back soon!")
        return
    dice=[]
    for i in range (0, lives):
        dice.extend(heartDie())
    while (lives >0):
        print(f"Lives remaining : {lives}")
        command=input("Select action (enter h for help or rules for rules): ").lower()
        match command:
            case "h" | "help":
                helpMessage()
            case "rules":
                rules()
            case "r" | "R"|"roll"| "Roll":
                rollAll(dice)
            case "e" | "E" | "Edit" | "edit":
                editDie(dice)
            case "a" | "A" | "Add" | "add":
                addDie(dice)
            case "d" | "D" | "display" | "Display":
                displayDice(dice)
            case "l" | "L" | "lose" | "Lose":
                lives=removeDie(dice)
            case "consume"|"c":
                consume(dice)
            case "reroll"|"Reroll":
                reroll(dice)
            case "f"|"freeze":
                freeze(dice)
            # case "blank" | "b" |"Blank" |"B":
            #     blankRandom(dice)
            case "random":
                randomSelect(dice)
            case "advan"|"advantage"|"adv":
                advantage(dice)
            # case "set"|"setroll":
            #     setRoll(dice)
            case "quit"| "q" | "cancel" :
                check=input("Are you sure you want to quit? What about your dice? \n")
                match check:
                    case "yes"| "y":
                        print("Come back soon!")
                        return
    print("You lost. Better luck next time!")




if __name__ == '__main__':
    main()
