#include <stdio.h>

typedef enum {
    ETAT_CLOSED,
    ETAT_SYN_SENT,
    ETAT_SYN_RECEIVED,
    ETAT_ESTABLISHED
} EtatTCP;

int main() {
    EtatTCP client = ETAT_CLOSED;
    EtatTCP serveur = ETAT_CLOSED;

    printf("Simulation du 3-way handshake TCP\n\n");

    // Étape 1 : le client envoie SYN
    printf("Client -> Serveur : SYN\n");
    client = ETAT_SYN_SENT;
    serveur = ETAT_SYN_RECEIVED;

    // Étape 2 : le serveur répond SYN-ACK
    printf("Serveur -> Client : SYN-ACK\n");

    // Étape 3 : le client répond ACK
    printf("Client -> Serveur : ACK\n");
    client = ETAT_ESTABLISHED;
    serveur = ETAT_ESTABLISHED;

    if (client == ETAT_ESTABLISHED && serveur == ETAT_ESTABLISHED) {
        printf("\nConnexion TCP établie.\n");
    } else {
        printf("\nErreur : connexion non établie.\n");
    }

    return 0;
}

// COMMANDES : 🔹 Compilation / exécution
// gcc tcp_sim.c -o tcp_sim
// ./tcp_sim
