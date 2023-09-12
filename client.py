import socket
import random
import threading

BUFFER_SIZE = 1024
HOST = 'localhost'
PORT = 5000

dest = (HOST, PORT)  

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('localhost', random.randint(8000, 9999)))

username = input('Bem vindo! Digite "hi, meu nome eh <nome_do_usuario>" para se conectar\n')

def receive_messages():
    finished = False
    while not finished:
        try:
            message, server_address = client.recvfrom(BUFFER_SIZE)
            if message.decode().endswith('entrou na sala!'):
                print(message.decode())
                contato, server_address = client.recvfrom(BUFFER_SIZE)
                ip_address, server_address = client.recvfrom(BUFFER_SIZE)
                contato = contato.decode()
                ip_address = ip_address.decode()
                contatos[contato] = ip_address
            else:    
                print(message.decode())
        except:
            pass

receive = threading.Thread(target=receive_messages)
receive.start()

client.sendto(username.encode(), dest)

contatos = {}

sending = True
while sending:
    message = input()         # nome do arquivo a ser enviado, lido pelo console
    if message == 'bye':
        exit()
    elif message == 'list':
        for name in contatos:
            print(name)
    else:
        client.sendto(message.encode(), dest)