import socket      # Pour créer une connexion TCP
import codecs      # Pour décoder ROT13
import re          # Pour extraire la chaîne entre apostrophes

# Adresse du challenge Root-Me
HOST = "challenge01.root-me.org"
PORT = 52021       # ⚠️ Port spécifique au challenge ROT13

# Connexion au serveur TCP
s = socket.socket()
s.connect((HOST, PORT))

# Lecture des données envoyées par le serveur
# Le serveur envoie plusieurs lignes, donc on lit un gros bloc
data = s.recv(4096).decode()
print("Reçu :\n", data)

# Le serveur envoie une ligne du type :
# my string is 'Gur synt vf 1234'
# On récupère ce qui est entre les apostrophes
match = re.search(r"'([^']+)'", data)

# Si aucune chaîne n'est trouvée, on arrête
if not match:
    print("Impossible de trouver la chaîne encodée.")
    exit()

# Récupération de la chaîne encodée
encoded = match.group(1)
print("Chaîne encodée :", encoded)

# Décodage ROT13
decoded = codecs.decode(encoded, "rot_13")
print("Décodé :", decoded)

# Envoi de la réponse au serveur
# IMPORTANT : il faut envoyer un retour à la ligne à la fin
s.send((decoded + "\n").encode())

# Lecture de la réponse finale (mot de passe)
print("Réponse du serveur :", s.recv(4096).decode())
