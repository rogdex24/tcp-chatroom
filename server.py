import socket
import threading


hostIP = socket.gethostname() # localhost
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((hostIP, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # if broadcast fails: i.e. conn. breaks w/  one client
            #     remove that client and close conn.
            index = clients.index(client)
            clients.remove(client)
            client.close()
            #     remove the nickname data
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break # end while loop and thread


def receive():
    while True:
        client, address = server.accept() # keep accepting connections
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))

        # add the client to the list
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickame of the client is {nickname} !')

        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        client.send('Connected to the server!'.encode('ascii'))

        # Thread for each client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"Server is listening on port {PORT} ...")
receive()

    



