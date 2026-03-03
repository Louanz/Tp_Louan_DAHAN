import unittest
from tp1_switch_router.python.network_devices import L2Switch, L3Switch

# Mocks simples pour simuler les trames et paquets
class MockEthernetFrame:
    def __init__(self, src, dst, packet=None):
        self.sourceMAC = src
        self.destinationMAC = dst
        self.packet = packet  # utilisé par L3Switch


class MockIPPacket:
    def __init__(self, src, dst):
        self.sourceIP = src
        self.destinationIP = dst


class TestL2Switch(unittest.TestCase):

    def test_learn_mac(self):
        sw = L2Switch()
        sw.learn_mac("AA:BB:CC:DD:EE:FF", 1)
        self.assertIn("AA:BB:CC:DD:EE:FF", sw.mac_table)
        self.assertEqual(sw.mac_table["AA:BB:CC:DD:EE:FF"], 1)

    def test_forward_known_mac(self):
        sw = L2Switch()
        sw.learn_mac("11:22:33:44:55:66", 3)
        frame = MockEthernetFrame("AA", "11:22:33:44:55:66")
        result = sw.forward(frame)
        self.assertEqual(result, "Forwarding frame to port 3")

    def test_forward_unknown_mac(self):
        sw = L2Switch()
        frame = MockEthernetFrame("AA", "FF:FF:FF:FF:FF:FF")
        result = sw.forward(frame)
        self.assertEqual(result, "Broadcasting frame")


class TestL3Switch(unittest.TestCase):

    def test_inheritance(self):
        sw = L3Switch()
        self.assertTrue(hasattr(sw, "mac_table"))
        self.assertTrue(hasattr(sw, "routing_table"))

    def test_add_route(self):
        sw = L3Switch()
        sw.add_route("192.168.", "next-hop-1")
        self.assertIn("192.168.", sw.routing_table)

    def test_route_found(self):
        sw = L3Switch()
        sw.add_route("10.0.", "router-A")
        packet = MockIPPacket("10.0.0.1", "10.0.5.12")
        result = sw.route(packet)
        self.assertEqual(result, "Routing packet to router-A")

    def test_route_not_found(self):
        sw = L3Switch()
        packet = MockIPPacket("10.0.0.1", "172.16.0.1")
        result = sw.route(packet)
        self.assertEqual(result, "No route found")

    def test_forward_ethernet_only(self):
        sw = L3Switch()
        frame = MockEthernetFrame("AA", "BB")
        result = sw.forward(frame)
        self.assertEqual(result, "Broadcasting frame")

    def test_forward_ip_packet(self):
        sw = L3Switch()
        sw.add_route("192.168.", "gateway-1")
        packet = MockIPPacket("192.168.1.10", "192.168.1.20")
        frame = MockEthernetFrame("AA", "BB", packet=packet)
        result = sw.forward(frame)
        self.assertEqual(result, "Routing packet to gateway-1")


if __name__ == "__main__":
    unittest.main()
