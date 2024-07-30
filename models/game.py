from.player import Player
import random
from enum import Enum

GameState = Enum('GameState', ['INIT', 'PLAYING', 'OVER'])

class Game:
    def __init__(self,startingLives, gameID):
        self.state= GameState.INIT
        self.id= gameID
        self.connections={}
        self.players=[]
        self.startingLives = startingLives
        self.loser= None
        self.round=0

    def addPlayer(self, pid, sid):
        self.players.append(Player(self.startingLives, pid))
        print(f"added {pid} to game {self.id} with sid {sid}")
        self.connections[pid]=sid
                

    def reconnectPlayer(self, pid, sid):
        self.connections[pid]=sid


    def removePlayer(self, pid):
        del self.connections[pid]
        target = None
        for player in self.players:
            if pid == player.uid:
                target= player
                break
        self.players.remove(target)
    def currPlayer(self):
        return self.players[self.currPlayerIndex]
    def nextPlayer(self):
        if self.currPlayerIndex==len(self.players)-1:
            self.currPlayerIndex=0
        else:
            self.currPlayerIndex+=1
        return self.players[self.currPlayerIndex]
    def run(self):
        #if len(self.players) <2:
           #raise Exception()
        random.shuffle(self.players)
        self.currPlayerIndex=0
        self.state=GameState.PLAYING
        return self.roundStart()

    def roundStart(self):
        self.round+=1
        msgs=[Response('message', f'Start of round {self.round}', self.id), Response('RoundStart', '', self.id)] +self.broadcastPlayersDice()
        self.oldBid=None
        for player in self.players:
            player.rollAll()
            msgs.append(Response('DiceRolls', player.getRolls(), self.connections[player.uid]))
        self.bidderIndex=0
        msgs=msgs +[Response('message', f'{self.currPlayer().uid}\'s turn', self.id),
            Response('GetBid', f"Asking {self.currPlayer().uid} for bid", self.connections[self.currPlayer().uid] )]
        print(f'This is what messages is returning\n {msgs}')
        return msgs

    def handleBid(self, player, bid):
        print("handling bid")
        print(f"looking for {self.currPlayer().uid} and getting message from {player}")
        if self.currPlayer().uid != player:
            print(f"err: not player {player}'s turn")
            return [Response("BidError", "Not player turn", self.connections[player])]
        try:
            self.checkBid(bid)
        except:
            print(f"err: not a valid bid of {bid.quantity} {bid.face}'s")
            return [Response("BidError", "Not valid bid", self.connections[player])]
        np = self.nextPlayer()
        self.oldBid = bid
        return[Response("BidAcknowledge", "bid successful", self.connections[player]),
        Response('PlayerBid', {'prevPlayer': player, 'prevFace' : bid.face, 'prevQuantity' :bid.quantity}, self.id),
        Response('message', f'{player} has bid {bid.quantity} {bid.face}\'s', self.id),
        Response('message', f'{np.uid}\'s turn', self.id),
         Response("GetBid", f"Asking {np.uid} for bid", self.connections[np.uid])]
        
    def challenge(self, player):
        if self.currPlayer().uid != player:
            return [Response("BidError", "Not player turn", self.connections[player])]
        if self.oldBid is None:
            return [Response("BidError", "No bid to challenge", self.connections[player])]
        bidder = self.players[self.bidderIndex]
        challenger = self.currPlayer()
        loser= None
        if(self.count()):
            loser = challenger
        else: 
            loser = bidder
        self.loser = loser
        print(f"loser for round {self.round} is {loser.uid}")
        return[Response('BidAcknowledge', 'Challenge accepted', self.connections[player]),
            Response("LoseDie", f"{loser.uid}, please select a die to lose", self.connections[loser.uid])]
    
    def handleLoseDie(self, player, dieIndex):
        if self.loser.uid != player:
            return [Response("BidError", "Not player turn", self.connections[player])]
        self.loser.lose(dieIndex)
        self.loser.lives-=1
        msgs = [Response("LoseDieAck","sucessfully lost a die", self.connections[player]),
            Response("message", f"Player {player} has lost a die", self.id)]
        if self.loser.lives == 0:
            msgs+=([Response("LoseGame", "You have lost the Game", self.connections[player]), Response("message", f"{player} has lost the game", self.id)])
            self.removePlayer(player)
        if len(self.players) == 1:
            msgs+=[ (Response("message", f"{self.players[0].uid} has won the game", self.id))]
            return msgs
        self.loser= None
        print(f'msgs before round start called {msgs}')
        msgs+= self.roundStart()
        print(f'msgs after round start called {msgs}')
        return msgs
    
  
    def playerList(self):
        result = []
        for player in self.players:
            result.append(player.uid)
        return result
        
  

    def count(self):
        face=self.oldBid.face
        total=0
        for player in self.players:
            rolls=player.getRolls()['count']
            total+=rolls[face]
        print(f'checking for {face}. {total} {face}\'s found against {self.oldBid.quantity}')
        return self.oldBid.quantity <= total

    def checkBid(self, newBid):
        
        print("checking bid")
        if self.oldBid is None:
            self.oldBid=newBid
            return
        oldBid=self.oldBid
        # if isinstance(newBid, SkipBid):
        #     return
        print(f"comparing bid when comparing old bid of {oldBid.quantity} {oldBid.face}'s to new bid of {newBid.quantity} {newBid.face}'s")
        if newBid.quantity> oldBid.quantity or newBid.face > oldBid.face:
            self.bidderIndex=self.currPlayerIndex
            self.oldBid=newBid
            return
        else:
            
            raise Exception()
    
    def broadcastPlayersDice(self):
        data=[]
        for player in self.players:
            data.append({'dice': player.dieInfo(),
                        'pid': player.uid
                                  })

        return [(Response('PlayersDiceInfo', data, self.id))]
    #checking state functions    
    def playing(self):
        return self.state== GameState.PLAYING
    def init(self):
        return self.state== GameState.INIT
    def over(self):
        return self.state==GameState.OVER
    
            

class Bid:
    def __init__(self, quantity, face):
        self.quantity=quantity
        self.face=face
    def quantity(self):
        return self.quantity
    def face(self):
        return self.face

class SkipBid(Bid):
    def __init__(self):
        return None

class Response:
    def __init__(self, message, body, recepient):
        self.msg = message
        self.data = body
        self.target = recepient


def setPlayerOrder(loser, players):
    startingPlayerIndex=players.index(loser)
    return players[startingPlayerIndex:]+players[:startingPlayerIndex]