# Topologie 2

## Techniques :
- VTP : Propage les vlans entre le Switch L3 et le 
- HSRP : Redondance de routeur en actif/passif
- ACL étendues : Règle de sécurité unidirectionnel
- DNS : Domain Name Service (/53) - Traduit IP en url et inversement
- DHCP : Dynamic Host Configuration Protocol (UDP/66 & UDP/67) - Attribue dynamiquement une IP
- Server Web


## ACLs :
- BLOCK_HTTP_IT_SERVER : Bloque le protocole HTTP (TCP/80) entre le vlan IT (21) et le vlan Server (30)
- ALLOW_TELNET_ROUTERS : Ajouter le Telnet pour se connecter aux Routeurs (192.168.0.1 & 192.168.0.2 sur Gig0/0/0)
- BLOCK_TELNET_MARKETING : Bloquer Telnet pour le service marketing (vlan 22)

### Warning :
Pour autoriser "ALLOW_TELNET_ROUTERS", il faut utiliser les VTY / Access-class d'après la documentation :
```
line vty 0 4
    password cisco
    login
    transport input telnet
    access-class ALLOW_TELNET_ROUTERS in
exit
```