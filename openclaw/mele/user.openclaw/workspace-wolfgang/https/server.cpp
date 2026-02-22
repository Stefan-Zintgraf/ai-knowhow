#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>

constexpr int PORT = 9090;
constexpr int BUFFER_SIZE = 4096;

int main() {
    int server_fd, client_fd;
    struct sockaddr_in address;
    int opt = 1;
    socklen_t addrlen = sizeof(address);
    char buffer[BUFFER_SIZE];

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        return 1;
    }

    // Set socket options
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt failed");
        return 1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind socket
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        return 1;
    }

    // Listen
    if (listen(server_fd, 10) < 0) {
        perror("listen failed");
        return 1;
    }

    std::cout << "Server running on http://localhost:" << PORT << std::endl;
    std::cout << "Press Ctrl+C to stop" << std::endl;

    while (true) {
        // Accept connection
        if ((client_fd = accept(server_fd, (struct sockaddr*)&address, &addrlen)) < 0) {
            perror("accept failed");
            continue;
        }

        // Read request
        ssize_t bytes_read = read(client_fd, buffer, BUFFER_SIZE - 1);
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Request received" << std::endl;
        }

        // Read index.html file
        std::string body;
        std::ifstream file("index.html");
        if (file.is_open()) {
            std::string line;
            while (std::getline(file, line)) {
                body += line + "\n";
            }
            file.close();
        } else {
            body = "<html><body><h1>Error: Could not load index.html</h1></body></html>";
        }

        // HTTP response
        std::string response =
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: " + std::to_string(body.length()) + "\r\n"
            "Connection: close\r\n"
            "\r\n" + body;

        send(client_fd, response.c_str(), response.length(), 0);
        close(client_fd);
    }

    close(server_fd);
    return 0;
}