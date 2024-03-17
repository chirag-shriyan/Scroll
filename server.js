const { Server } = require("socket.io");
const http = require('http');
const httpServer = http.Server();

const io = new Server(httpServer,{
    cors: {
        origin: '*'
    }
});

io.on("connection", (socket) => {

    const roomIds = [].concat(JSON.parse(socket.handshake.query.roomIds));
    const username = socket.handshake.query.username;

    // console.log(`Socket Id: ${socket.id} | username: ${username}`);

    roomIds.forEach(roomId => {
        if (roomId) {
            socket.join(roomId);
        }
    });

    socket.on('message', (data) => {
        const { message, message_id } = data
        console.log('Received data: ', data);
        io.to(roomIds).emit('message', { id: socket.id, message: message, message_id: message_id });

        io.emit('notifications', { username: username});

    });


});

httpServer.listen(3000)
// io.listen(3000);