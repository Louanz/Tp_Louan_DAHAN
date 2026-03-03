class Workstation:
    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ipAddress = ip


class User:
    def __init__(self, username, role, workstation: Workstation):
        self.username = username
        self.role = role
        self.workstation = workstation

    def login(self):
        return f"{self.username} logged into {self.workstation.hostname}"

    def logout(self):
        return f"{self.username} logged out"
