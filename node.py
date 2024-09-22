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

    def FindFile(self, request, context):
        filename_hash = hashlib.sha1(request.filename.encode()).hexdigest()
        node_addresses = self.dht.get(filename_hash, [])
        return p2p_pb2.FileResponse(node_addresses=node_addresses)

    def Join(self, request, context):
        print(f"Node {request.node_address} joined the network")
        return p2p_pb2.JoinResponse(success=True)

    def Leave(self, request, context):
        print(f"Node {request.node_address} left the network")
        return p2p_pb2.LeaveResponse(success=True)

def serve(node_address, dht):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p2p_pb2_grpc.add_P2PNodeServicer_to_server(P2PNode(node_address, dht), server)
    server.add_insecure_port(node_address)
    server.start()
    print(f"Node running at {node_address}")
    return server

def connect_to_node(node_address, target_node_address):
    channel = grpc.insecure_channel(target_node_address)
    stub = p2p_pb2_grpc.P2PNodeStub(channel)
    join_request = p2p_pb2.JoinRequest(node_address=node_address)
    stub.Join(join_request)
    print(f"Connected to {target_node_address}")

def find_file(filename, target_node_address):
    channel = grpc.insecure_channel(target_node_address)
    stub = p2p_pb2_grpc.P2PNodeStub(channel)
    file_request = p2p_pb2.FileRequest(filename=filename)
    response = stub.FindFile(file_request)
    return response.node_addresses
