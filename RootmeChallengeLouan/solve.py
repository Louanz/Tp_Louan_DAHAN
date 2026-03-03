import socket      # Permet de créer une connexion réseau (TCP)
import base64      # Pour décoder les chaînes Base64
import codecs      # Pour décoder ROT13
import re          # Pour extraire la chaîne encodée avec une regex

# Adresse et port du challenge Root-Me
HOST = "challenge01.root-me.org"
PORT = 52023

# Fonction qui tente plusieurs décodages possibles
def decode_auto(s):
    # 1) Tentative Base64
    try:
        return base64.b64decode(s).decode()
    except:
        pass  # Si ça échoue, on continue

    # 2) Tentative ROT13
    try:
        return codecs.decode(s, "rot_13")
    except:
        pass

    # 3) Tentative Hexadécimal
    try:
        return bytes.fromhex(s).decode()
    except:
        pass

    # Si aucun décodage ne marche
    return None

# Création de la socket TCP
s = socket.socket()

# Connexion au serveur du challenge
s.connect((HOST, PORT))

# Lecture des données envoyées par le serveur
# Le serveur envoie plusieurs lignes, donc on lit un gros bloc
data = s.recv(4096).decode()
print("Reçu :\n", data)

# Le serveur envoie une ligne du type :
# my string is 'XXXXX'
# On récupère ce qui est entre les apostrophes
match = re.search(r"'([^']+)'", data)

# Si aucune chaîne n'est trouvée, on arrête
if not match:
    print("Impossible de trouver la chaîne encodée.")
    exit()

# Récupération de la chaîne encodée
encoded = match.group(1)
print("Chaîne encodée :", encoded)

# Décodage automatique
decoded = decode_auto(encoded)
print("Décodé :", decoded)

# Envoi de la réponse au serveur
# IMPORTANT : il faut envoyer un retour à la ligne à la fin
s.send((decoded + "\n").encode())

# Lecture de la réponse finale (mot de passe)
print("Réponse du serveur :", s.recv(4096).decode())
