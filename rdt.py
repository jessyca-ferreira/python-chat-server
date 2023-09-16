import pickle
import socket

class RDTChannel():
    
    BUFFER_SIZE = 1024

    def __init__(self, host, type='') -> None:
        self.host = host
        self.type = type
        self.active_connections = {}

    def rdt_send(self, message, destination):
        if destination not in self.active_connections:
            self.active_connections[destination] = {'ack': 1, 'seq' : 0}
            
        sndpkt = pickle.dumps((self.active_connections[destination]['ack'], self.active_connections[destination]['seq'], message))      # make_pkt com campos (ack, seq, data)
        self.host.sendto(sndpkt, destination)       
        self.host.settimeout(5)
        self.wait_for_ack(sndpkt, self.active_connections[destination]['seq'], destination)
        
        self.active_connections[destination]['ack'] ^= 1
        self.active_connections[destination]['seq'] ^= 1

        return
    
    def wait_for_ack(self, sndpkt, expected_ack, destination):        
        waiting = True
        while waiting:
            try:
                rcvpkt, address = self.host.recvfrom(self.BUFFER_SIZE)
                data = pickle.loads(rcvpkt)        # extract_pkt
                
                current_ack = data[0]
                message = data[2]

                if (current_ack == expected_ack and message == 'ACK' and address == destination):
                    self.host.settimeout(None)
                    waiting = False
                    return
                    
            except socket.timeout:
                self.host.sendto(sndpkt, destination)
                self.host.settimeout(5)
            
    def rdt_receive(self):
        waiting = True
        while waiting:
            rcvpkt, address = self.host.recvfrom(self.BUFFER_SIZE)
            data = pickle.loads(rcvpkt)
            
            if address not in self.active_connections:
                self.active_connections[address] = {'ack': 1, 'seq' : 0}

            current_seq = data[1]
            expected_seq = self.active_connections[address]['seq']
            
            if (current_seq == expected_seq):
                waiting = False
                sndpkt = pickle.dumps((current_seq, current_seq ^ 1, 'ACK'))      # make_pkt com campos (ack, seq, data)
                self.host.sendto(sndpkt, address)
                self.active_connections[address]['ack'] ^= 1
                self.active_connections[address]['seq'] ^= 1
                return data, address
            else:
                return None, None
    

            
        
            

