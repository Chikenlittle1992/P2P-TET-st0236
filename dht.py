import hashlib

class DHT:
    def __init__(self):
        self.table = {}  # Tabla de archivos
        self.routing_table = {}  # Tabla de enrutamiento (vecinos)

    def add_file(self, filename, node_address):
        file_hash = hashlib.sha1(filename.encode()).hexdigest()
        if file_hash not in self.table:
            self.table[file_hash] = []
        self.table[file_hash].append(node_address)

    def remove_node(self, node_address):
        for file_hash in self.table:
            self.table[file_hash] = [node for node in self.table[file_hash] if node != node_address]

        # También remover el nodo de la tabla de enrutamiento
        self.routing_table = {k: v for k, v in self.routing_table.items() if v != node_address}

    def get(self, file_hash, default=[]):
        return self.table.get(file_hash, default)

    def add_neighbor(self, node_address, neighbor_address):
        # Añade un vecino a la tabla de enrutamiento si no está ya
        if node_address not in self.routing_table:
            self.routing_table[node_address] = []
        if neighbor_address not in self.routing_table[node_address]:
            self.routing_table[node_address].append(neighbor_address)

    def get_neighbors(self, node_address):
        # Devuelve los vecinos del nodo actual
        return self.routing_table.get(node_address, [])
