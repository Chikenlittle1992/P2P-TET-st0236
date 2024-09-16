import grpc
from concurrent import futures
import threading
import dht_network_pb2
import dht_network_pb2_grpc

class DhtNode(dht_network_pb2_grpc.DhtServiceServicer):
    def __init__(self,node_id: int, ip: str, port: int):
        self.node_id = node_id
        self.ip = ip
        self.port = port
        self.files = {} #Storage files on this node
        self.nodes = {} #Dictionary of known nodes in the network
    
    #Rpc methods
    def PutFile(self, request, context):
        self.files[request.filename] = request.content
        return dht_network_pb2.FileResponse(message = "File stored succesfully", content = request.content)

    def GetFile(self, request, context):
        content = self.files.get(request.filename, "")
        if content:
            return dht_network_pb2.FileResponse(message="File found", content=content)
        else:
            return dht_network_pb2.FileResponse(message="File found", content="")
        
    def LookupFile(self, request, context):
        if request.filename in self.files:
            return dht_network_pb2.LocationResponse(node_id=self.node_id, filename=request.filename)
        return dht_network_pb2.LocationResponse(node_id=-1, filename="")

    def JoinNetwork(self, request, context):
        self.nodes[request.node_id] = (request.ip, request.port)
        return dht_network_pb2.Confirmation(node_id=request.node_id, message="Node joined the network")

    def LeaveNetwork(self, request, context):
        if request.node_id in self.nodes:
            del self.nodes[request.node_id]
            return dht_network_pb2.Confirmation(node_id=request.node_id, message="Node left the network")
        return dht_network_pb2.Confirmation(node_id=request.node_id, message="Node not found in the network")

    def start(self):
        #start gRPC server for this node
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        dht_network_pb2_grpc.add_DhtServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{self.ip}:{self.port}')
        server.start()
        print(f'Node {self.node_id} listening on {self.ip}:{self.port}')
        server.wait_for_termination()
    

    def join_network(self, bootstrap_ip, bootstrap_port):
        # Connect to bootstrap node and join the network
        channel = grpc.insecure_channel(f'{bootstrap_ip}:{bootstrap_port}')
        stub = dht_network_pb2_grpc.DhtServiceStub(channel)
        response = stub.JoinNetwork(dht_network_pb2.JoinRequest(node_id=self.node_id, ip=self.ip, port=self.port))
        print(f'JoinNetwork Response: {response.message}')

    def leave_network(self, bootstrap_ip, bootstrap_port):
        # Notify bootstrap node to leave the network
        channel = grpc.insecure_channel(f'{bootstrap_ip}:{bootstrap_port}')
        stub = dht_network_pb2_grpc.DhtServiceStub(channel)
        response = stub.LeaveNetwork(dht_network_pb2.LeaveRequest(node_id=self.node_id))
        print(f'LeaveNetwork Response: {response.message}')

if __name__ == '__main__':
    node_id = 1
    ip = '127.0.0.1'
    port = '50051'
    node = DhtNode(node_id, ip, port)

    # Start the node server in a separate thread
    server_thread = threading.Thread(target=node.start)
    server_thread.start()

    # Example: Join an existing network using a bootstrap node
    bootstrap_ip = '127.0.0.1'
    bootstrap_port = '50051'
    node.join_network(bootstrap_ip, bootstrap_port)