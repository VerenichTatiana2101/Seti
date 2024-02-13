# Необходимо написать программу-клиент, 
# которая будет цепляться к вашему серверу в Интернете. 
# Послем того как соединение произошло, 
# первое сообщение будет ником пользователя, а далее, 
# любое отправленное сообщение будет транслироваться другим клиентам. 
# Таким образом пообщаемся между собой.

import socket
import threading
import logging

# Настройка логирования
logging.basicConfig(filename='server_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#данные для подключения
host = '127.0.0.1'
port = 55555

#стартуем сервер
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
                logging.error(f"Error in handle(): {e}")
                print(f"Error in handle(): {e}")
                # Removing And Closing Clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

# Listening Function
def receive():
    try:
        while True:
            # Accept Connection
            client, address = server.accept()
            logging.info(f"Connected with {address}")

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            logging.info(f"Nickname is {nickname}")
            broadcast(f"{nickname} joined!".encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    finally:
        for client in clients:
            try:
                client.close()  # Закрываем соединения с клиентами
            except Exception as e:
                logging.error(f"Error closing client connection: {e}")
        server.close()

print("Server if listening...")
receive()