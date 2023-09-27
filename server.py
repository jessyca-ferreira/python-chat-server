import socket
import queue
import datetime
import rdt      # importa o canal rdt criado no aquivo rdt.py

LOCALHOST = socket.gethostbyname(socket.gethostname())
ORIGIN = (LOCALHOST, 5000)
host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host.bind(ORIGIN)

server = rdt.RDTChannel(host, 'SERVER')

messages = queue.Queue()
clients = {}

def receive():
    try:
        data, address = server.rdt_receive()
        message = data[2]
        
        if message != 'ACK':
            messages.put((message, address))
    except:
        pass

def send():
    if not messages.empty():
        message, address = messages.get()
        time = get_date_time()
        if address not in clients.keys() and message != 'ACK':
            clients[address] = message[15:].strip()
            
            for client in clients.copy():
                text = f'{message[15:].strip()} entrou na sala!'

                server.rdt_send(text, client)
        else:
            if message == 'list':
                # broadcast da lista de conexões
                text = ''.join(
                    f'{key[0]}/{key[1]} - {clients[key]}\n' for key, value in server.active_connections.items() if value['state'] != 0
                )
                server.rdt_send(('list', text), address)
            elif message == 'bye':
                server.rdt_send(message, address)
                del server.active_connections[address]
            else:
                for client in clients.copy():
                    try:
                        text = f"{address[0]}:{address[1]}/~{clients[address]}: {message} {time}"
                        server.rdt_send(text, client)
                    except:
                        del clients[address]             

def get_date_time():
    current_date_time = datetime.datetime.now()
    date_time = current_date_time.strftime("%m/%d/%Y, %H:%M:%S")    
    return date_time 
    
finished = False
while not finished:
    receive()
    send()
