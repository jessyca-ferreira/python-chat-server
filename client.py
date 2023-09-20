import socket
import random
import threading
import sys
import rdt      # importa o canal rdt criado no aquivo rdt.py

LOCALHOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
ORIGIN = (LOCALHOST, random.randint(8000, 9999))

destination = (LOCALHOST, PORT)  

host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host.bind(ORIGIN)

client = rdt.RDTChannel(host)
contatos = {}

def receive():
    while True:
        try:
            data, address = client.rdt_receive()     # tupla (ack, seq, data)
            message = data[2]            
            
            if message == 'bye':
                print('Você foi desconectado')
                host.close()
                break
            elif message[0] == 'list':       
                for x in message[1].split('\n'):
                    contatos[x[:14]] = x[17:]
                        
                print(message[1])
            else:
                print(message)
        except:
            pass
    
def send():
    while True:
        message = input()               
        client.rdt_send(message, destination)
        if message == 'bye':
            break

username = ''
while not username.startswith('hi, meu nome eh'):
    username = input('Bem vindo! Digite "hi, meu nome eh <nome_do_usuario>" para se conectar\n')

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()

client.rdt_send(username, destination)       
    