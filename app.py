from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_cors import CORS
from models.server import *
from models.game import *

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


games = {} #map game code -> game
players={} #map pid to game code
# @app.route("/<game_id>")
# def gameAction(game_id):
#     return 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_game', methods=['POST'])
def make_game():
    data = request.get_json()
    print(f"data{data}")
    lives = int(data['lives'])
    print(lives)
    gameCode= generateRoomCode()
    while generateRoomCode in games.keys():
        gameCode= generateRoomCode()
    print(f"Gamecode: {gameCode}")
    games[gameCode]= Game(lives, gameCode)
    #print(f"SID: {request.sid}"
    return jsonify({"game_id": gameCode})

@app.route('/login', methods=['GET'])
def login():
    data = request.get_json()
    uid = data['uid']
    res= {"inGame": False}
    if uid in players.keys():
        res['inGame']= True
        rid =players[uid]
        game = games[rid]
        game.reconnectPlayer(uid, request.sid)
    return jsonify(res)

@socketio.on('makeGame')
def socketGame(data):
    print(f"data{data}")
    lives = int(data['lives'])
    user = data['username']
    print(lives)
    gameCode= generateRoomCode()
    while generateRoomCode in games.keys():
        gameCode= generateRoomCode()
    print(f"Gamecode: {gameCode}")
    game= Game(lives, gameCode)
    games[gameCode]=game
    #print(f"SID: {request.sid}"
    join_room(gameCode)
    game.addPlayer(user, request.sid)
    players[user] = gameCode
    emit('joinGame',gameCode, to= request.sid)
    send(f"{user} has joined the game {gameCode}.", room=gameCode)
    emit('lobbyUpdate', game.playerList(), room=gameCode)
    

@socketio.on('joinGame')
def on_join(data):
    username = data['username']
    room = data['room']
    #pid = data['pid']
    print(f"username: {username} \nroom: {room}")
    if username in players.keys():
        emit("joinError", "Already in a game", to =request.sid)
    elif room in games:
        join_room(room)
        #games.setdefault(game_id, []).append(username)
        
        game = games[room]
        if username in game.connections.keys():
            send(f"{username} has already joined game {room}", room = room)
        else:
            
            print(request.sid)
            game.addPlayer(username, request.sid)
            players[username]=room
            emit('joinGame',room, to= request.sid)
            send(f"{username} has joined the game {room}.", room=room)
            emit('lobbyUpdate', game.playerList(), room=room)
    else:
        emit("joinError", "Room not found", to =request.sid)
    


@socketio.on('leaveGame')
def on_leave(data):

    username = data['username']
    print(f"player {username} leaving game")
    game_id = players[username]
    auth(username, game_id)
    game = games[game_id]
    leave_room(game_id)
    game.removePlayer(username)
    del players[username]
    send(f"{username} has left the game {game_id}.", room=game_id)
    emit('lobbyUpdate', game.playerList(), room=game_id)
    if (len(game.players)==0):
        del games[game_id]
        print(f"deleting game {game_id}")
    emit('leaveGame', "Successfully left game", to = request.sid)

@socketio.on('startGame')
def on_start(data):
    username = data['username']
    game_id = players[username]
    game = games[game_id]
    #game.run()
    emit('startGame', f"Game {game_id} has started", room =game_id)
    sendMSGS(game.run())

@socketio.on('sendBid')
def on_bid(data):
    username = data['username']
    quantity = data['quantity']
    face = data['face']
    rid=players[username]
    print(f"{username} submitted a bid of {quantity} {face}'s")
    bid = Bid(int(quantity), int(face))
    auth(username, rid)
    game = games[rid]
    sendMSGS(game.handleBid(username, bid))

@socketio.on('challengeBid')
def challenge_bid(data):
    username =data['username']
    rid=players[username]
    auth(username, rid)
    game=games[rid]
    sendMSGS(game.challenge(username))
    

@socketio.on('message')
def handle_message(data):
    print(f"getting data: {data}" )
    game_id = data['game_id']
    message = data['message']
    send(message, room=game_id)

@socketio.on('LoseDie')
def handleLoseDie(data):
    username=data['username']
    dieIndex=data['dieIndex']
    rid = players[username]
    auth(username, rid)
    game=games[rid]
    sendMSGS(game.handleLoseDie( username, dieIndex))

def auth(uid, rid):
    if uid not in players.keys() or players[uid] != rid:
        raise Exception()

def sendMSGS(msgs):
    print(msgs)
    for msg in msgs:
        print(f"sending message of type {msg.msg} to {msg.target}")
        emit(msg.msg, msg.data, to=msg.target)


if __name__ == "__main__":
    app.run(debug=True)