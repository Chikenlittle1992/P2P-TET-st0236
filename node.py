import grpc
from concurrent import futures
import p2p_pb2
import p2p_pb2_grpc
from dht import DHT
import hashlib
import random
import time

class P2PNode(p2p_pb2_grpc.P2PNodeServicer):
    def __init__(self, node_address, dht):
        self.node_address = node_address
        self.dht = dht
        self.neighbors = {}  # Diccionario para almacenar los vecinos

    def FindFile(self, request, context):
        filename_hash = hashlib.sha1(request.filename.encode()).hexdigest()
        node_addresses = self.dht.get(filename_hash, [])
        return p2p_pb2.FileResponse(node_addresses=node_addresses)

    def Join(self, request, context):
        # Agregar el nodo que se está uniendo como vecino
        if request.node_address != self.node_address:
            self.neighbors[request.node_address] = request.node_address
        print(f"Nodo {request.node_address} se ha unido a la red")
        return p2p_pb2.JoinResponse(success=True)

    def Leave(self, request, context):
        # Remover el nodo de la lista de vecinos
        if request.node_address in self.neighbors:
            del self.neighbors[request.node_address]
        print(f"Nodo {request.node_address} se ha desconectado de la red")
        return p2p_pb2.LeaveResponse(success=True)

    def GetNeighbors(self, request, context):
        # Devolver los vecinos actuales
        return p2p_pb2.NeighborsResponse(neighbors=list(self.neighbors.keys()))

def serve(node_address, dht):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p2p_pb2_grpc.add_P2PNodeServicer_to_server(P2PNode(node_address, dht), server)
    server.add_insecure_port(node_address)
    server.start()
    print(f"Nodo corriendo en {node_address}")
    return server

def connect_to_node(node_address, target_node_address):
    # Conectarse al nodo de destino
    channel = grpc.insecure_channel(target_node_address)
    stub = p2p_pb2_grpc.P2PNodeStub(channel)
    
    # Enviar solicitud de unión
    join_request = p2p_pb2.JoinRequest(node_address=node_address)
    stub.Join(join_request)
    print(f"Conectado a {target_node_address}")
    
    # Obtener vecinos del nodo al que te has conectado
    neighbors = get_neighbors(target_node_address)
    
    # Actualizar vecinos locales con los del nodo de destino
    update_neighbors(node_address, neighbors)

    # También informar a los nuevos vecinos sobre este nodo
    for neighbor in neighbors:
        update_neighbors(neighbor, [node_address])  # Propagar la información del nuevo nodo

def find_file(filename, target_node_address):
    channel = grpc.insecure_channel(target_node_address)
    stub = p2p_pb2_grpc.P2PNodeStub(channel)
    file_request = p2p_pb2.FileRequest(filename=filename)
    response = stub.FindFile(file_request)
    return response.node_addresses

def get_neighbors(target_node_address):
    channel = grpc.insecure_channel(target_node_address)
    stub = p2p_pb2_grpc.P2PNodeStub(channel)
    response = stub.GetNeighbors(p2p_pb2.NeighborsRequest())
    return response.neighbors

def update_neighbors(node_address, neighbors):
    """Actualizar la lista de vecinos en todos los nodos vecinos"""
    for neighbor_address in neighbors:
        channel = grpc.insecure_channel(neighbor_address)
        stub = p2p_pb2_grpc.P2PNodeStub(channel)
        join_request = p2p_pb2.JoinRequest(node_address=node_address)
        stub.Join(join_request)
        print(f"Actualizando a {neighbor_address} con nuevo vecino: {node_address}")
