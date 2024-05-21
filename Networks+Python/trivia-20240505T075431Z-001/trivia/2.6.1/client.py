import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP,SERVER_PORT))
    return my_socket

def error_and_exit(error_msg):
    print("Error has occurred.")
    exit(1)


def recv_message_and_parse(conn):
    data = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(data)
    return cmd, data

def build_and_send_message(conn, code, data):
    full_msg = chatlib.build_message(code, data)
    print(full_msg)
    return conn.send(full_msg.encode())


def login(conn):
    connected = False
    while not connected:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], (username, password))
        cmd, data = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful!")
            connected = True
        else:
            print("Login failed. Please try again.")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Logged out. Bye.")
    conn.close()



def main():
    try:
        conn = connect()  # Establish connection first
        login(conn)      # Use the connection for login
        logout(conn)     # Logout after successful login (assuming this is desired)
    except ConnectionRefusedError:
        print("Connection failed. Server might be down.")
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        if conn:  # Close the connection if it exists
            conn.close()



if __name__ == '__main__':
    main()
