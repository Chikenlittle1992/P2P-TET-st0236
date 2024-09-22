import hashlib

class DHT:
    def __init__(self):
        self.table = {}

    def add_file(self, filename, node_address):
        file_hash = hashlib.sha1(filename.encode()).hexdigest()
        if file_hash not in self.table:
            self.table[file_hash] = []
        self.table[file_hash].append(node_address)

    def remove_node(self, node_address):
        for file_hash in self.table:
            self.table[file_hash] = [node for node in self.table[file_hash] if node != node_address]

    def get(self, file_hash, default=[]):
        return self.table.get(file_hash, default)
