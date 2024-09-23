import grpc
from concurrent import futures

import dht_network_pb2
import dht_network_pb2_grpc


class dht_network(dht_network_pb2_grpc.DhtServiceServicer):
    def __init__(self, node):
        self.node = node


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

    def serve(self):
        #start gRPC server for this node
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        dht_network_pb2_grpc.add_DhtServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{self.ip}:{self.port}')
        server.start()
        print(f'Node {self.node_id} listening on {self.ip}:{self.port}')
        server.wait_for_termination()