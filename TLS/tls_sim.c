#include <stdio.h>

int main() {
    printf("Simulation d'une négociation TLS (simplifiée)\n\n");

    printf("Client -> Serveur : ClientHello\n");
    printf("Serveur -> Client : ServerHello\n");
    printf("Serveur -> Client : Certificate\n");
    printf("Client -> Serveur : ClientKeyExchange\n");
    printf("Client -> Serveur : ChangeCipherSpec + Finished\n");
    printf("Serveur -> Client : ChangeCipherSpec + Finished\n");

    printf("\nCanal TLS établi (simulation).\n");

    return 0;
}


// gcc tls_sim.c -o tls_sim
// ./tls_sim
