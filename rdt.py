import pickle
import socket
import threading

class RDTChannel():
    
    BUFFER_SIZE = 1024
    lock = threading.Lock()

    def __init__(self, host, type='') -> None:
        self.host = host
        self.type = type
        self.active_connections = {}
        self.state = ''
        self.sndpkt = ''

    def rdt_send(self, message, destination):
        if destination not in self.active_connections:
            self.active_connections[destination] = {'ack': 1, 'seq' : 0, 'state': 0}
            
        if self.active_connections[destination]['state'] != 'wait_for_ack':
            
            self.sndpkt = pickle.dumps((self.active_connections[destination]['ack'], self.active_connections[destination]['seq'], message))      # make_pkt com campos (ack, seq, data)
            self.host.sendto(self.sndpkt, destination)       
            self.active_connections[destination]['state'] = 'wait_for_ack'
            if self.type == 'SERVER':
                print(f'SERVER: ENVIADO PACOTE \033[1;3m ACK {self.active_connections[destination]["ack"]} SEQ {self.active_connections[destination]["seq"]} \033[0m')
            self.host.settimeout(5)

        return
            
    def rdt_receive(self):
        waiting = True
        while waiting:
            rcvpkt, address = self.host.recvfrom(self.BUFFER_SIZE)
            data = pickle.loads(rcvpkt)        # extract_pkt
            
            if address not in self.active_connections:
                self.active_connections[address] = {'ack': 1, 'seq' : 0, 'state' : 0}
                
            if self.active_connections[address]['state'] == 'wait_for_ack':
                try:                    
                    message = data[2]
                    current_ack = data[0]
                    expected_ack = self.active_connections[address]['seq']
                    if (current_ack == expected_ack and message == 'ACK'):
                        self.host.settimeout(None)
                        self.active_connections[address]['state'] = 'receive'
                        if self.type == 'SERVER':
                            print(f'SERVER: RECEBIDO \033[1;3m ACK {self.active_connections[address]["ack"]} \033[0m')
                        self.active_connections[address]['ack'] ^= 1
                        self.active_connections[address]['seq'] ^= 1
                        waiting = False

                        return
                        
                except socket.timeout:
                    self.host.sendto(self.sndpkt, address)
                    self.host.settimeout(5)
            else:
                current_seq = data[1]
                expected_seq = self.active_connections[address]['seq']
                if self.type == 'SERVER':
                    print(f'CLIENTE {address[0]}/{address[1]} ESTÁ ENVIANDO PACOTE \033[1;3m ACK {self.active_connections[address]["ack"]} SEQ {self.active_connections[address]["seq"]} \033[0m')

                
                if (current_seq == expected_seq):
                    if self.type == 'SERVER':
                        print(f'SERVER: RECEBIDO PACOTE \033[1;3m ACK {self.active_connections[address]["ack"]} SEQ {self.active_connections[address]["seq"]} \033[0m')
                    sndpkt = pickle.dumps((current_seq, current_seq ^ 1, 'ACK'))      # make_pkt com campos (ack, seq, data)
                    self.host.sendto(sndpkt, address)
                    self.active_connections[address]['ack'] ^= 1
                    self.active_connections[address]['seq'] ^= 1
                    waiting = False
                    return data, address


            
        
            

