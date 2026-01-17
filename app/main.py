class Dictionary:
    def __init__(self, capacity=8, load_factor=0.6):
        self.capacity = capacity
        self.load_factor = load_factor
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        bucket = self.hash_table[index]
        if bucket is not None:
            for k, v in bucket:
                if k == key:
                    return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            self.hash_table[index] = []

        bucket = self.hash_table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                break
        else:
            bucket.append((key, value))
            self.size += 1
            self.check_load_factor()

    def __len__(self):
        return self.size

    def items(self):
        result = []
        for bucket in self.hash_table:
            if bucket is not None:
                for key, value in bucket:
                    result.append((key, value))
        return result

    def check_load_factor(self):
        if self.size / self.capacity >= self.load_factor:
            self.resize()

    def resize(self):
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity

        for bucket in self.hash_table:
            if bucket is not None:
                for key, value in bucket:
                    index = hash(key) % new_capacity
                    new_bucket = new_hash_table[index]
                    if new_bucket is None:
                        new_bucket = []
                        new_hash_table[index] = new_bucket
                    new_bucket.append((key, value))

        self.capacity = new_capacity
        self.hash_table = new_hash_table
