import socket

def main():
    s_socket = socket.socket()
    s_socket.bind(('0.0.0.0', 8820))
    s_socket.listen()
    print("Server up and running")
    c_socket, c_address = s_socket.accept()
    data = c_socket.recv(1024).decode()
    print("Client sent: " + data)
    c_socket.send(data.encode())
    c_socket.close()
    s_socket.close()


if __name__ == "__main__":
    main()

