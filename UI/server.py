import threading
import socket

host = '127.0.0.1'
port = 6543

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            print(f"Message from {message.decode('utf-8')}")
            broadcast(message)
        except:
            break

    # Remove client from lists and notify others
    if client in clients:
        clients.remove(client)
    nickname = nicknames.pop(clients.index(client)) if client in clients else "Unknown"
    broadcast(f'{nickname} left the chat!'.encode('utf-8'))
    client.close()

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client_{len(clients)} is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()
