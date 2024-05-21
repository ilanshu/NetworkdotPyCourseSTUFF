import socket
import datetime
import random
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")

(client_socket, client_address) = server_socket.accept()
print("Client connected")

data = client_socket.recv(1024).decode()

if data == 'time':
    reply = datetime.datetime.now()
    client_socket.send(str(reply).encode())

elif data == 'whoru':
    reply = 'shimshon'
    client_socket.send(reply.encode())

elif data == 'rand':
    reply = random.randint(1,10)
    client_socket.send(str(reply).encode())

elif data == 'exit':
    client_socket.send('Bye'.encode())
    client_socket.close()
    server_socket.close()

client_socket.close()
server_socket.close()