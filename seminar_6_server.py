# в библиотеке всё необходимое для создания сокетов
from time import sleep
import socket
# многопоточность
import threading

# по умолчанию сокет создаётся tcp в адресном пространстве ipv4
# если нужно что-то поменять, 

# т.к коннект через https порт 443
# через cmd пингуем ya.ru копируем ip

ya_socket = socket.socket()
addr = ("5.255.255.242", 443)
ya_socket.connect(addr)

# запрос на сервер яндекс
data_out = b"GET / HTTP/1.1\r\nHost:ya.ru\r\n\r\n"
ya_socket.send(data_out)

# перехват данных и печать, указывая размер буфера для хранения(кратный 2 и небольшой)
# data_in = ya_socket.recv(1024)
# print(data_in)
# # таким образом ответ можно разбить на куски поэтому это лучше делать циклом
# data_in = ya_socket.recv(1024)
# print(data_in)
# data_in = ya_socket.recv(1024)
# print(data_in)
# data_in = ya_socket.recv(1024)
# print(data_in)
# data_in = ya_socket.recv(1024)
# print(data_in)
# data_in = ya_socket.recv(1024)
# print(data_in)

data_in = b""

def recieving():
    global data_in
    while True: 
        data_chunk = ya_socket.recv(1024)
        data_in = data_in + data_chunk

# создадим поток
rec_thread = threading.Thread(target=recieving)
# запустить поток
rec_thread.start()

sleep(4)
print(data_in)
ya_socket.close()