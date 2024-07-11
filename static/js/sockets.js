

socket.on('message', function(msg) {
    const messagesDiv = document.getElementById('messages');
    const newMessage = document.createElement('div');
    newMessage.textContent = msg;
    messagesDiv.appendChild(newMessage);
});

function joinGame() {
    const username = document.getElementById('username').value;
    const game_id = document.getElementById('game_id').value;
    socket.emit('join', {username: username, game_id: game_id});
}

function leaveGame() {
    const username = document.getElementById('username').value;
    const game_id = document.getElementById('game_id').value;
    socket.emit('leave', {username: username, game_id: game_id});
}

function sendMessage() {
    const game_id = document.getElementById('game_id').value;
    const message = document.getElementById('message').value;
    socket.emit('message', {game_id: game_id, message: message});
}