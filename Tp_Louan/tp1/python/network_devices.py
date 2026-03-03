class L2Switch:
    def __init__(self):
        self.mac_table = {}

    def learn_mac(self, mac, port):
        self.mac_table[mac] = port

    def forward(self, frame):
        dest = frame.destinationMAC
        if dest in self.mac_table:
            return f"Forwarding frame to port {self.mac_table[dest]}"
        return "Broadcasting frame"


class L3Switch(L2Switch):
    def __init__(self):
        super().__init__()
        self.routing_table = {}

    def add_route(self, network, next_hop):
        self.routing_table[network] = next_hop

    def route(self, packet):
        dest = packet.destinationIP
        for network, next_hop in self.routing_table.items():
            if dest.startswith(network):
                return f"Routing packet to {next_hop}"
        return "No route found"

    def forward(self, frame):
        # Polymorphisme : même nom, comportement différent
        if hasattr(frame, "packet"):
            return self.route(frame.packet)
        return super().forward(frame)
