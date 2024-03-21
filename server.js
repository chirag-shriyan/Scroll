const { Server } = require("socket.io");
const http = require('http');
const httpServer = http.Server();

const io = new Server(httpServer, {
    cors: {
        origin: '*'
    }
});

io.on("connection", (socket) => {

    socket.on('join_rooms', (data) => {
        socket.join(data);
    });

    socket.on('message', async (data) => {
        const { message, message_id, roomId ,userId } = data;

        io.to(roomId).emit('message', { id: socket.id, message: message, message_id: message_id, roomId: roomId });

        if (userId !== undefined){
            console.log(userId);
            io.emit('notifications', { userId: userId + roomId, roomId });
        }
        else{
            io.to(roomId).emit('notifications', { roomId });
        }

    });

    socket.on('typing', (data) => {
        const { roomId } = data;
        if (roomId) {
            io.to(roomId).emit('typing', { roomId ,isTyping: true ,userId:socket.id});
        }
    });

});

httpServer.listen(3000,'192.168.100.5');
// httpServer.listen(3000);