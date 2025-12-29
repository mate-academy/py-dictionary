class Dictionary:
    def __init__(self):
        self.table = [[] for _ in range(8)]
        self.size = 0
    
    def __setitem__(self, key, value):
        hash_value = hash(key)
        index = hash_value % len(self.table)
        bucket = self.table[index]

        for i, node in enumerate(bucket):
            existing_key = node[0]
            if existing_key == key:
                bucket[i] = (key, hash_value, value)
                return
            
        bucket.append((key, hash_value, value))
        self.size += 1

        if self.size / len(self.table) > 0.7:
            self._resize()

    def __getitem__(self, key):
        hash_value = hash(key)
        index = hash_value % len(self.table)
        bucket = self.table[index]

        for node in bucket:
            existing_key = node[0]
            if existing_key == key:
                return node[2]
        raise KeyError(key)

    def __len__(self):
        return self.size

    def get(self, key, default=None):
        hash_value = hash(key)
        index = hash_value % len(self.table)
        bucket = self.table[index]

        for node in bucket:
            if node[0] == key:
                return node[2]
        return default
    
    def clear(self):
        current_capacity = len(self.table)
        self.table = [[] for _ in range(current_capacity)]
        self.size = 0
    
    def __delitem__(self, key):
        hash_value = hash(key)
        index = hash_value % len(self.table)
        bucket = self.table[index]

        for i, node in enumerate(bucket):
            if node[0] == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(key)
    
    def _resize(self):
        old_table = self.table
        new_capacity = len(old_table) * 2
        self.table = [[] for _ in range(new_capacity)]
        self.size = 0

        for bucket in old_table:
            for node in bucket:
                key = node[0]
                hash_value = node[1]
                value = node[2]
                new_index = hash_value % new_capacity
                self.table[new_index].append((key, hash_value, value))
                self.size += 1