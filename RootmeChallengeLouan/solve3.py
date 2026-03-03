import socket
import base64
import zlib
import re

HOST = "challenge01.root-me.org"
PORT = 52022

s = socket.socket()
s.connect((HOST, PORT))

while True:
    data = s.recv(4096).decode()

    # Si le serveur envoie le mot de passe
    if "Password" in data:
        print(data)
        break

    print("Reçu :\n", data)

    # Extraction de la chaîne encodée
    encoded_match = re.search(r"'([^']+)'", data)
    if not encoded_match:
        print("Aucune chaîne trouvée.")
        break

    encoded = encoded_match.group(1)

    # Extraction du nombre de répétitions
    repeat_match = re.search(r"(\d+)\s+time", data)
    if repeat_match:
        repeat = int(repeat_match.group(1))
    else:
        # Si le serveur ne précise pas, par défaut il faut envoyer 1 fois
        repeat = 1

    # Décodage base64 + zlib
    decoded = zlib.decompress(base64.b64decode(encoded)).decode()

    print("Message décompressé :", decoded)
    print("Répétitions demandées :", repeat)

    # Construction de la réponse
    response = ((decoded + "\n") * repeat).encode()

    # Envoi
    s.send(response)
