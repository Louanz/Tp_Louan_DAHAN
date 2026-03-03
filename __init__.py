@startuml

class EthernetFrame {
  - destinationMAC : String
  - sourceMAC : String
  - etherType : int
}

class IPPacket {
  - sourceIP : String
  - destinationIP : String
  - ttl : int
}

class L2Switch {
  - macTable : dict
  + learnMAC(mac, port)
  + forward(frame : EthernetFrame)
}

class L3Switch {
  - routingTable : dict
  + route(packet : IPPacket)
  + forward(frame : EthernetFrame)
}

EthernetFrame --> IPPacket : encapsule >
L2Switch --> EthernetFrame : traite >
L3Switch --> IPPacket : route >
L3Switch --|> L2Switch

@enduml
