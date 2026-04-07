const WebSocket = require('ws');

const server = new WebSocket.Server({ port: 8080 });

server.on('connection', socket => {
  console.log("Client connecté");

  socket.on('message', msg => {
    console.log("Reçu :", msg.toString());
    socket.send("Echo: " + msg);
  });
});

console.log("Serveur WebSocket sur ws://localhost:8080");

