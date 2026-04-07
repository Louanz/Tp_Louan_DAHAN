// Bibliothèques standard d'entrée/sortie
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

// Pour inet_addr(), conversion IP, structures réseau
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

int main(int argc, char *argv[]) {

    // Vérifie que l'utilisateur a bien fourni une adresse IP
    if (argc != 2) {
        printf("Usage: %s <IP>\n", argv[0]);
        return 1;
    }

    // Récupère l'adresse IP passée en argument
    char *target_ip = argv[1];

    // Définition de la plage de ports à scanner
    int start_port = 1;
    int end_port = 1024;

    // Structure contenant les informations de connexion
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;                 // IPv4
    addr.sin_addr.s_addr = inet_addr(target_ip); // Convertit l'IP en format binaire

    // Boucle sur tous les ports de la plage
    for (int port = start_port; port <= end_port; port++) {

        // Création d'un socket TCP
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) continue; // Si erreur, on passe au port suivant

        // Définit le port à tester (conversion en big-endian)
        addr.sin_port = htons(port);

        // Tentative de connexion au port
        int result = connect(sock, (struct sockaddr *)&addr, sizeof(addr));

        // Si connect() retourne 0 → connexion réussie → port ouvert
        if (result == 0) {
            printf("Port %d ouvert\n", port);
        }

        // On ferme le socket avant de passer au suivant
        close(sock);
    }

    return 0;
}
