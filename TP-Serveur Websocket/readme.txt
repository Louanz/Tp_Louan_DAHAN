
Tutoriel WebSocket, Wireshark et Burp Suite

1) Serveur WebSocket
Installer Node.js puis exécuter :
npm init -y
npm install ws

Créer server.js :
const WebSocket = require('ws');
const server = new WebSocket.Server({ port: 8080 });
server.on('connection', s => {
  s.on('message', m => s.send("Echo: " + m));
});
Lancer : node server.js

2) Client WebSocket
Créer client.html :
<script>
  const ws = new WebSocket("ws://localhost:8080");
  ws.onopen = () => ws.send("Hello !");
  ws.onmessage = e => console.log(e.data);
</script>

3) Analyse avec Wireshark
Choisir l’interface Wi-Fi ou Ethernet.
Si le serveur et le client sont en localhost, choisir "Adapter for loopback traffic capture".
Filtre conseillé : tcp.port == 8080
Observer le handshake WebSocket et les frames échangées.

4) Analyse avec Burp Suite
Configurer le navigateur en proxy : 127.0.0.1:8080
Ouvrir le client WebSocket.
Dans Burp, aller dans Proxy > WebSockets.
Visualiser, modifier et rejouer les frames.
