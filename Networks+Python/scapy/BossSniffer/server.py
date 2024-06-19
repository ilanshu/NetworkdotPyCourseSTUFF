import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'

correct_password = 'moneyIsLife'  # the correct password


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def login():
    # starting point - not logged in, then lets the boss log in (works only when correct password entered)
    logged = False
    while not logged:
        user_password = input("Enter password: ").strip()
        if user_password == correct_password:
            logged = True
        else:
            print("Wrong password.")

    return logged

def setup_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Server is up and running, listening for clients...")
    return server_socket


def accept_new_client(server_socket, client_sockets):
    client_socket, client_address = server_socket.accept()
    print("New client joined!", client_address)
    client_sockets.append(client_socket)
    print_client_sockets(client_sockets)
    return client_sockets

def handle_client_message(current_socket, client_sockets):
    try:
        data = current_socket.recv(MAX_MSG_LENGTH).decode()
        if data == "":
            print("Connection closed")
            client_sockets.remove(current_socket)
            current_socket.close()
            print_client_sockets(client_sockets)
        elif "Blacklisted site detected" in data:
            client_address = current_socket.getpeername()
            print(f"{data}, Theft occurred on {client_address[0]}")
    except ConnectionResetError:
        print("Connection closed abruptly")
        client_sockets.remove(current_socket)
        current_socket.close()
        print_client_sockets(client_sockets)
    return client_sockets

def main():
    if login():
        print("Setting up server...")
        server_socket = setup_server()
        client_sockets = []

        while True:
            ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
            for current_socket in ready_to_read:
                if current_socket is server_socket:
                    client_sockets = accept_new_client(server_socket, client_sockets)
                else:
                    client_sockets = handle_client_message(current_socket, client_sockets)


if __name__ == "__main__":
    main()
