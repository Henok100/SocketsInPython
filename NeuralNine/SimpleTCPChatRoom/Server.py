import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())     #get address
PORT = 9000                                                                        
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(5)

clients = []
nicknames = []  #names of clients

#Broadcast to all
def broadcast(message):
    for client in clients:
        client.send(message)

#Handle clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode(FORMAT))
            nicknames.remove(nickname)
            break

#Accpet Clients all the time
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode(FORMAT))
        client.send("Connected to the server".encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server is Listening...")
receive()