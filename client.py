import socket
import threading

target = socket.gethostname()
PORT = 1234

nickname = input("Type in your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Make TCP Connection
client.connect((target, PORT))

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred!')
            client.close()
            break

def write():
    while True:

        message = f"{nickname}: {input('')}"
        
        client.send(message.encode('ascii'))

# Threads run in parallel so sending and receiveing keep working

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()