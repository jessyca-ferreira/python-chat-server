import socket
import threading
import queue
import datetime
from pathlib import Path

BUFFER_SIZE = 1024
ORIGIN = ('localhost', 5000)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ORIGIN)

def receive_messages():
    finished = False
    while not finished:
        try:
            message, client_address = server.recvfrom(BUFFER_SIZE)
            messages.put((message, client_address))
        except:
            pass

def send_messages():
    finished = False
    while not finished:
        while not messages.empty():
            message, addr = messages.get()
            time = get_date_time()
            message = message.decode()
            if addr not in clients.keys():
                while not message.startswith('hi, meu nome eh'):
                    message, client_address = server.recvfrom(BUFFER_SIZE)
                    message = message.decode()
                clients[addr] = message[15:].strip()
                for client in clients.copy():
                    server.sendto((f'{message[15:]} entrou na sala!').encode(), client)
                    server.sendto(message[15:].strip().encode(), client)
                    server.sendto(addr[0].encode(), client)
            else:    
                for client in clients.copy():
                    try:
                        text = f"{addr[0]}:{addr[1]}/~{clients[addr]}: {message} {time}".encode()
                        server.sendto(text, client)
                    except:
                        del clients[addr]

                    

def get_date_time():
    current_date_time = datetime.datetime.now()
    date_time = current_date_time.strftime("%m/%d/%Y, %H:%M:%S")    
    return date_time

messages = queue.Queue()
clients = {}
                        
receive = threading.Thread(target=receive_messages)
send = threading.Thread(target=send_messages)

receive.start()
send.start()
