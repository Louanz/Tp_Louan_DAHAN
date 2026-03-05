import { createServer } from "http";
import { Server } from "socket.io";

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: "*"
  }
});

io.on("connection", (socket) => {
    console.log("🎉 Nouveau client connecté :", socket.id);

    // 1) Message direct au client
    setTimeout(() => {
        socket.emit("sport", 
            '"Pitoyables", "une saison de gifles"... la presse médusée par le nouveau sabordage de l\'OM en Coupe de France"'
        );
    }, 3000);

    // 2) Message de bienvenue
    socket.emit("welcome", `Bienvenue ${socket.id}, prêt pour le chaos ? 😄`);

    // 3) Broadcast aux autres clients
    socket.broadcast.emit("new-user", `Un nouveau client vient d'arriver : ${socket.id}`);

    // 4) Réception d’un message du client
    socket.on("ping", (msg) => {
        console.log(`📩 ping reçu de ${socket.id} :`, msg);
        socket.emit("pong", "pong bien reçu !");
    });

    // 5) Déconnexion
    socket.on("disconnect", () => {
        console.log("❌ Client déconnecté :", socket.id);
        socket.broadcast.emit("user-left", `${socket.id} a quitté le serveur`);
    });
});

httpServer.listen(3000, () => {
    console.log("🚀 WebSocket server running on http://localhost:3000");
});
