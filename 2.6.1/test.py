from socket import socket, AF_INET, SOCK_STREAM

# Define server port (same as in chatlib.py)
PORT = 5678

def handle_client(conn):
  """
  Handles communication with a connected client.
  """
  print("Client connected!")
  while True:
    # Receive data from the client
    data = conn.recv(1024).decode()
    if not data:
      break

    # Parse the received message
    cmd, msg = chatlib.parse_message(data)

    # Handle login request
    if cmd == "LOGIN":
      # Simulate login check (replace with your actual logic)
      if msg == "valid_username#valid_password":
        response = chatlib.build_message("LOGIN_OK", "")
        conn.send(response.encode())
      else:
        response = chatlib.build_message("ERROR", "Invalid credentials")
        conn.send(response.encode())
    else:
      print(f"Received unexpected command: {cmd}")

    # Exit loop on any other message (assuming login test)
    break

  conn.close()
  print("Client disconnected!")

def main():
  """
  Starts the mock server and listens for connections.
  """
  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind(("", PORT))
  server_socket.listen(1)

  print(f"Mock server listening on port {PORT}")
  while True:
    conn, addr = server_socket.accept()
    print(f"Client connected from {addr}")
    handle_client(conn)

if __name__ == "__main__":
  import chatlib  # Assuming chatlib.py is in the same directory
  main()
