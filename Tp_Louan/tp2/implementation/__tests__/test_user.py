import unittest
from tp2_user_workstation.python.user import User, Workstation


class TestWorkstation(unittest.TestCase):

    def test_workstation_initialization(self):
        ws = Workstation("PC-01", "192.168.1.10")
        self.assertEqual(ws.hostname, "PC-01")
        self.assertEqual(ws.ipAddress, "192.168.1.10")


class TestUser(unittest.TestCase):

    def setUp(self):
        self.ws = Workstation("PC-01", "192.168.1.10")
        self.user = User("alice", "admin", self.ws)

    def test_user_initialization(self):
        self.assertEqual(self.user.username, "alice")
        self.assertEqual(self.user.role, "admin")
        self.assertIs(self.user.workstation, self.ws)

    def test_login(self):
        result = self.user.login()
        self.assertEqual(result, "alice logged into PC-01")

    def test_logout(self):
        result = self.user.logout()
        self.assertEqual(result, "alice logged out")


if __name__ == "__main__":
    unittest.main()


# commande d'execution test : python -m unittest discover -s tp2_user_workstation/tests
