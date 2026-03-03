# ACLs — Projet Packet Tracer

Configuration des Access Control Lists pour le réseau **shadows** (VTP domain).
Tous les fichiers sont à appliquer sur un **routeur en inter-VLAN routing**.

---

## Plan d'adressage

| VLAN | Nom | Réseau |
|------|-----------|------------------|
| 20 | Marketing | 192.168.20.0/24 |
| 21 | IT | 192.168.21.0/24 |
| 22 | Direction | 192.168.22.0/24 |
| 30 | Server | 192.168.30.0/24 |

---

## Fichiers de configuration

### `acl1_block_marketing.config`
**ACL Standard — Bloquer Marketing vers les Serveurs**

Empêche tout le trafic du VLAN Marketing (20) d'atteindre le VLAN Server (30).
Les autres VLANs (IT, Direction) conservent un accès normal aux serveurs.
L'ACL est appliquée en `in` sur la sous-interface `GigabitEthernet0/0.30`.

---

### `acl2_it_ssh_only.config`
**ACL Étendue — Seul IT peut accéder aux serveurs en SSH**

Autorise uniquement le VLAN IT (21) à établir des connexions SSH (port 22) vers les serveurs.
Tout autre trafic à destination du VLAN Server (30) est bloqué, quelle que soit la source.
L'ACL est appliquée en `in` sur la sous-interface `GigabitEthernet0/0.30`.

---

### `acl3_policy_internet.config`
**ACL Étendue — Politique d'accès différenciée par VLAN**

Applique deux niveaux d'accès différents :
- **Direction (VLAN 22)** : accès total à tous les réseaux et services.
- **Marketing (VLAN 20)** : limité au HTTP (port 80) et HTTPS (port 443) uniquement.
- Tout autre trafic Marketing est bloqué.

L'ACL est appliquée en `in` sur la sous-interface `GigabitEthernet0/0.20`.

---

### `acl4_no_ping.config`
**ACL Étendue — Bloquer ICMP entre VLANs (sauf IT)**

Interdit les pings entre VLANs pour tous les utilisateurs, à l'exception du VLAN IT (21) qui conserve la capacité de pinguer pour des raisons d'administration réseau.
L'ACL est appliquée en `in` sur les sous-interfaces des VLANs 20, 22 et 30.

---

### `acl5_vty_access.config`
**ACL Standard — Restreindre l'accès SSH/Telnet au VLAN IT**

Protège les lignes VTY du routeur (accès SSH et Telnet) en n'autorisant que les machines du VLAN IT (21) à s'y connecter.
Toute tentative de connexion depuis Marketing, Direction ou Server est refusée.
L'ACL est appliquée via `access-class` sur les lignes `vty 0 4`.

---

## Commandes utiles

```cisco
! Vérifier les ACLs et leurs hits
show ip access-lists

! Vérifier l'ACL appliquée sur une interface
show ip interface GigabitEthernet0/0.20

! Supprimer une ACL d'une interface
interface GigabitEthernet0/0.20
 no ip access-group POLICY_INTERNET in

! Supprimer une ACL complètement
no ip access-list extended POLICY_INTERNET
```

---

## Ordre d'application recommandé

1. `acl1_block_marketing.config` — test basique de blocage
2. `acl4_no_ping.config` — vérification ICMP
3. `acl2_it_ssh_only.config` — contrôle d'accès SSH
4. `acl3_policy_internet.config` — politique globale par VLAN
5. `acl5_vty_access.config` — sécurisation de l'administration

> **Attention** : ne pas appliquer plusieurs ACLs sur la même interface dans le même sens (`in` ou `out`) — une seule ACL par sens par interface.