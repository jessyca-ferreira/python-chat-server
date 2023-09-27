import socket
import random
import threading
import rdt      # importa o canal rdt criado no aquivo rdt.py

LOCALHOST = socket.gethostbyname(socket.gethostname()) # endereço de IP local do cliente
PORT = 5000
ORIGIN = (LOCALHOST, random.randint(8000, 9999)) # tupla com  o LOCALHOST e uma porta de número aleatório entre os valores especificados

destination = (LOCALHOST, PORT)

host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host.bind(ORIGIN)

client = rdt.RDTChannel(host) # cria um canal de comunicação rdt
contatos = {}

# funçoes receive e send
def receive():
    while True:
        try:
            data, address = client.rdt_receive()     # tupla (ack, seq, data)
            message = data[2]         
            
            if message == 'bye': # usuario desconectado caso a message seja igual a 'bye'
                print('Você foi desconectado')
                host.close()
                break
            elif message[0] == 'list': # imprime lista de conexões
                for x in message[1].split('\n'):
                    contatos[x[:14]] = x[17:]
                        
                print(message[1])
            else:
                print(message)
        except:
            pass
    
def send():
    while True:
        message = input() # mensagem a ser enviada               
        client.rdt_send(message, destination) # envia mensagem pelo canal rdt3.0
        if message == 'bye':
            break

username = '' # recebe nome do usuario
while not username.startswith('hi, meu nome eh'):
    username = input('Bem vindo! Digite "hi, meu nome eh <nome_do_usuario>" para se conectar\n') 

# iniciando threads
t1 = threading.Thread(target=receive) 
t2 = threading.Thread(target=send)

t1.start()
t2.start()

client.rdt_send(username, destination)  # começa a conexao       
    