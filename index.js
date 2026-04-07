// Import des modules nécessaires
const express = require('express');              // Framework HTTP minimaliste
const { createServer } = require('node:http');   // Serveur HTTP natif
const { join } = require('node:path');           // Pour gérer les chemins de fichiers
const { Server } = require('socket.io');         // Serveur Socket.IO
const sqlite3 = require('sqlite3');              // Driver SQLite
const { open } = require('sqlite');              // Promesses pour SQLite
const { availableParallelism } = require('node:os'); // Nombre de CPU dispo
const cluster = require('node:cluster');         // Permet de lancer plusieurs workers
const { createAdapter, setupPrimary } = require('@socket.io/cluster-adapter'); // Adapter cluster pour Socket.IO

// --- MODE CLUSTER : PROCESSUS PRINCIPAL ---
if (cluster.isPrimary) {
  const numCPUs = availableParallelism(); // Nombre de workers = nombre de cœurs CPU

  // On lance un worker par CPU, chacun avec un port différent
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork({
      PORT: 3000 + i // Chaque worker écoute sur un port unique
    });
  }

  console.log(`server running at http://localhost:3000`); // Affiché une seule fois
  return setupPrimary(); // Configure l’adapter cluster pour synchroniser les workers
}

// --- MODE WORKER : CHAQUE PROCESSUS LANCE SON SERVEUR ---
async function main() {
  // Ouverture de la base SQLite
  const db = await open({
    filename: 'chat.db',
    driver: sqlite3.Database
  });

  // Création de la table des messages (si elle n'existe pas)
  await db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,  // ID auto-incrémenté
      client_offset TEXT UNIQUE,             // Identifiant unique du message (anti-doublon)
      content TEXT                           // Contenu du message
    );
  `);

  const app = express();
  const server = createServer(app);

  // Initialisation de Socket.IO avec :
  // - récupération d'état (messages manqués)
  // - adapter cluster pour synchroniser les workers
  const io = new Server(server, {
    connectionStateRecovery: {},
    adapter: createAdapter()
  });

  // Route principale → renvoie la page HTML
  app.get('/', (req, res) => {
    res.sendFile(join(__dirname, 'index.html'));
  });

  // --- LOGIQUE SOCKET.IO ---
  io.on('connection', async (socket) => {

    // Réception d'un message du client
    socket.on('chat message', async (msg, clientOffset, callback) => {
      let result;

      try {
        // Tentative d'insertion dans la base
        result = await db.run(
          'INSERT INTO messages (content, client_offset) VALUES (?, ?)',
          msg,
          clientOffset
        );
      } catch (e) {
        // Erreur 19 = contrainte UNIQUE → message déjà inséré
        if (e.errno === 19 /* SQLITE_CONSTRAINT */) {
          callback(); // On confirme quand même au client
        }
        return; // On stoppe ici
      }

      // Broadcast du message à tous les clients
      io.emit('chat message', msg, result.lastID);

      callback(); // Accusé de réception
    });

    // Si le client n'a pas récupéré son état (déconnexion, refresh…)
    if (!socket.recovered) {
      try {
        // On renvoie tous les messages qu'il a manqués
        await db.each(
          'SELECT id, content FROM messages WHERE id > ?',
          [socket.handshake.auth.serverOffset || 0],
          (_err, row) => {
            socket.emit('chat message', row.content, row.id);
          }
        );
      } catch (e) {
        // En cas d'erreur, on ignore
      }
    }
  });

  // Chaque worker écoute sur son port dédié
  const port = process.env.PORT;
  server.listen(port); // Pas de console.log ici pour éviter le spam
}

main();
