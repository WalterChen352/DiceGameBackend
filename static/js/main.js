document.addEventListener('DOMContentLoaded', 
    ()=>{
        new App();
    });



class App{
    constructor(){
        this.socket = io();
        this.socket.on('message', (msg) => {
            console.log(msg);
        });
        this.socket.on('joinError', (msg)=>{
            console.log(msg);
        });
        this.socket.on('joinGame', (msg)=>{
            console.log("received confirmation")
            const lobby = document.querySelector('#lobby')
            lobby.classList.add('inLobby')
            lobby.classList.remove('notInLobby')
        });
        this.socket.on('LeaveGame', (msg)=>{
            console.log(msg)
            const lobby =document.querySelector('#lobby')
            lobby.classList.remove('inLobby')
            lobby.classList.add('notInLobby')
        });
        this.socket.on('GetBid', (msg)=>{
            console.log(msg)
            console.log("getting bid")
            const Game = document.getElementById('Game')
            Game.classList.add('PlayerTurn')
        });
        this.socket.on('BidAcknowledge', ()=>{
            const Game = document.getElementById('Game')
            Game.classList.remove('PlayerTurn')
        });
        this.socket.on('BidError', (msg)=> console.log(msg));
        this.socket.on('gameStart', (msg)=>console.log(msg));
        this.socket.on('Dice', (msg)=>console.log(msg));
        console.log('content loaded');
        const makeGameForm = document.querySelector('#makeGameForm');
        makeGameForm.addEventListener('submit', this.makeGame.bind(this));
        const body = document.querySelector('body');
        const loginForm = document.querySelector('#login form');
        loginForm.addEventListener('submit', this.login);
        console.log(localStorage.getItem('uid'));
        if (localStorage.getItem('uid')!== null){
            body.classList.add('loggedIn');
            // const loginData = await fetch('/login',{

            // });
        }
        else
            body.classList.add('loggedOut');
        const joinGameForm = document.querySelector('#joinGameForm');
        joinGameForm.addEventListener('submit', this.joinRoom.bind(this));
        const leaveGameButton = document.querySelector('#LeaveGame')
        leaveGameButton.addEventListener('click', this.leaveRoom.bind(this));
        const startGameButton = document.querySelector('#StartGame');
        startGameButton.addEventListener('click', this.startGame.bind(this));
        const bidForm = document.querySelector('#bidForm');
        bidForm.addEventListener('submit', this.bid.bind(this));
    }
    login(event){
        event.preventDefault();
        const formData = new FormData(event.target); 
        const uid = formData.get('username');
        localStorage.setItem('uid', uid);
        console.log(uid);
        const body =document.querySelector('body')
        body.classList.add('loggedIn');
        body.classList.remove('loggedOut');
    }
    joinRoom(event){
        event.preventDefault();
        const uid = localStorage.getItem('uid');
        console.log(uid);
        const rid = new FormData(event.target).get('gameInput');
        console.log(rid)
        this.socket.emit('join', {username: uid, room: rid});
    }

    async makeGame(event){
        event.preventDefault();
        event.target.reset()
        console.log('making game');
        const StartingLives = new FormData(event.target).get("startingLives");
        const res = await fetch('/make_game', {
            method: 'POST',
            headers: {
                 'Content-Type': 'application/json',
            },
             body:JSON.stringify({
                uid: localStorage.getItem('uid'), 
                lives: StartingLives
             })
        });
        if (!res.ok) { // Check if response is not OK
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const resData = await res.json();
        console.log(resData)
        const uid=localStorage.getItem('uid')
        const rid=resData['game_id']
        this.socket.emit('join', {username: uid, room: rid});
    }

    leaveRoom(event){
        event.preventDefault();
        const uid=localStorage.getItem('uid')
        this.socket.emit('leave', {username: uid})
    }

    startGame(event){
        event.preventDefault();
        const uid =localStorage.getItem('uid')
        this.socket.emit('start', {username: uid})
    }

    bid(event){
        event.preventDefault();
        const data = new FormData(event.target)
        const quantity = data.get('bidQuantity')
        const face = data.get('bidFace')
        const uid=localStorage.getItem('uid')
        this.socket.emit('bid', {username: uid, quantity: quantity, face: face})
    }

}







const makeGameReq = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    } // Adjust this as needed
};



