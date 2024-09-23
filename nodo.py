import grpc
from concurrent import futures
import threading
import dht_network_pb2 as pb2
import dht_network_pb2_grpc as pb2_grpc
import hashlib
import time

def hash_key(key: str):
    return int(hashlib.sha1(key.encode()).hexdigest(),16)%(2**16)

class Nodo():
    def __init__(self, node_id: int, ip: str, port: int, update_interval: int, config: dict):
        self.id = node_id
        self.ip = ip
        self.port = port
        self.succesor = self
        self.predecessor = None
        self.files = {}
        self.update_interval = update_interval
        self.finger_table = []  #inicializamos la finger table vacía
        self.init_finger_table()  #y luego la llenamos

    def init_finger_table(self):
        #we start the finger tables with ourselves as the first node
        m = 16
        for i in range(m):
            start = (self.id + 2**i) % (2**m)
            self.finger_table.append((start, self))

    def update_finger_table(self):
        m = 16
        for i in range(m):
            start = (self.id + 2**i) % (2**m)
            with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
                stub = pb2_grpc.DhtServiceStub(channel)
                self.finger_table[i] = (start, stub.FindSuccesor(pb2.Node(node_id=start)))
    
    def closest_finger(self, node_id: int):
        for i in range(len(self.finger_table)-1,-1,-1):
            if self.id < self.finger_table[i][1].id < node_id:
                return self.finger_table[i][1]
    

    def stabilize(self):
        while True:
            try:
                if self.succesor == self:
                    print("")
                else:
                    with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
                        stub = pb2_grpc.DhtServiceStub(channel)
                        temp = stub.FindSuccesor(pb2.Node(id=self.succesor.id)).id
                        if temp != self.succesor.id and ((self.id < temp < self.succesor.id) or ((self.id > self.succesor.id) and (temp > self.id or temp < self.succesor.id))):
                            self.succesor = temp
                            print(f"Nodo {self.id}, nuevo sucesor {temp}")
                        #stub.Notify(pb2.Node(id = self.id, ip=self.ip, port=self.port))
                    self.update_finger_table()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(self.update_interval)