#include <string>
#include <iostream>

class Workstation {
private:
    std::string hostname;
    std::string ipAddress;

public:
    Workstation(std::string host, std::string ip)
        : hostname(host), ipAddress(ip) {}
};

class User {
private:
    std::string username;
    std::string role;
    Workstation* workstation;

public:
    User(std::string name, std::string r, Workstation* ws)
        : username(name), role(r), workstation(ws) {}

    void login() {
        std::cout << username << " logged in." << std::endl;
    }

    void logout() {
        std::cout << username << " logged out." << std::endl;
    }
};
