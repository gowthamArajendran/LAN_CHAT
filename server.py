import socket
import threading

# Connection Data
HOST = '0.0.0.0'  # Ella network la irunthum connect aagalam
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass # Error aanal ignore pannalam temporarily

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break

def receive():
    print(f"Server is listening on Port {PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()