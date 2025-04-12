const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

io.on('connection', (socket) => {
    console.log('User connected');

    socket.on('registerUser', (username) => {
        socket.username = username;
        socket.broadcast.emit('userJoined', username);
    });

    socket.on('chatMessage', (msg) => {
        msg.id = Date.now();
        io.emit('newMessage', msg);
    });

    socket.on('disconnect', () => {
        if (socket.username) {
            io.emit('userLeft', socket.username);
        }
    });
});

http.listen(3000, () => {
    console.log('Socket.io server running on port 3000');
});