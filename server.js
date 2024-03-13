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

    console.log(`roomId: ${roomIds} | username: ${username}`);


    roomIds.forEach(roomId => {
        // console.log(roomId);
        if (roomId) {
            socket.join(roomId);
        }
    });

    socket.on('message', (data) => {
        console.log('Received data: ', data);
        io.to(roomIds).emit('message', { id: socket.id, message: data });

    });


});

httpServer.listen(3000, '192.168.100.5')
// io.listen(3000);