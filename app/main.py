class Dictionary:
    _BUCKET_INIT_SIZE = 8
    _BUCKET_LOAD_FACTOR = 2 / 3

    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.hash = hash(key)

        def __repr__(self):
            return f"(hash={self.hash}, key={self.key})"

    def _init_bucket(self, size: int) -> None:
        self.count = 0
        self.capacity = size
        self.threshold =\
            int(self.capacity * self.__class__._BUCKET_LOAD_FACTOR)
        self.bucket = [None] * self.capacity

    def _resize(self, new_size: int) -> None:
        if new_size <= self.capacity:
            raise ValueError("New size must be greater than current one")

        old_bucket = self.bucket

        self._init_bucket(new_size)

        for node in old_bucket:
            if not node:
                continue

            for i in self._scan_bucket(node.hash):
                if self.bucket[i] is None:
                    self.bucket[i] = node
                    self.count += 1
                    break

    def _scan_bucket(self, node_hash: int):
        node_index = node_hash % self.capacity
        scan_range = [(node_index, self.capacity)]
        if node_index != 0:
            scan_range.append((0, node_index))

        for i1, i2 in scan_range:
            for i in range(i1, i2):
                yield i

    def _seek_bucket(self, node_key) -> _Node:
        node_hash = hash(node_key)

        for i in self._scan_bucket(node_hash):
            node = self.bucket[i]

            if node is None:
                return None

            if node.hash == node_hash and node.key == node_key:
                return node

    def clear(self) -> None:
        self._init_bucket(self.__class__._BUCKET_INIT_SIZE)

    def get(self, key, value):
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key):
        node = self._seek_bucket(key)

        if node:
            self.bucket[self.bucket.index(node)] = None
            self.count -= 1
            return node.value

        raise KeyError(f"Key <{key}> not found in dictionary")

    def __delitem__(self, key):
        self.pop(key)

    def __getitem__(self, key):
        node = self._seek_bucket(key)

        if node:
            return node.value

        raise KeyError(f"Key <{key}> not found in dictionary")

    def __init__(self):
        self._init_bucket(self.__class__._BUCKET_INIT_SIZE)

    def __iter__(self):
        self.it = 0
        return self

    def __len__(self):
        return self.count

    def __next__(self):
        while True:
            if self.it >= self.capacity:
                raise StopIteration

            node = self.bucket[self.it]
            self.it += 1

            if node:
                return node.key

    def __setitem__(self, key, value):
        node = self._seek_bucket(key)

        if node:
            node.value = value
            return

        if self.count == self.threshold:
            self._resize(self.capacity * 2)

        node = self._Node(key, value)

        for i in self._scan_bucket(node.hash):
            if self.bucket[i] is None:
                self.bucket[i] = node
                self.count += 1
                return
