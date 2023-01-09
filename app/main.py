class Dictionary:
    def get_hash_table_index_for(self, key_hash):
        return key_hash % self.capacity

    def increase_hash_table_index_by_one(self, hash_table_index):
        hash_table_index += 1
        hash_table_index %= self.capacity
        return hash_table_index

    def return_threshold(self):
        return int(self.capacity * 2 / 3)

    def setup_hash_table(self):
        return [[] for _ in range(self.capacity)]

    def clear_hash_table_cell(self, hash_table_index):
        self.hash_table[hash_table_index] = []

    def write_to_hash_table(self, hash_table_index, item):
        self.hash_table[hash_table_index] = item

    def is_hash_table_cell_empty(self, hash_table_index):
        if self.hash_table[hash_table_index]:
            return False
        return True

    def are_keys_equal(self, hash_table_index, key):
        if key == self.hash_table[hash_table_index][0]:
            return True
        return False

    def update_hash_table_value(self, hash_table_index, item):
        self.hash_table[hash_table_index][2] = item[2]

    def find_cell_by_hash_and_key(self, hash_table_index, key):
        if not self.is_hash_table_cell_empty(hash_table_index):
            while True:
                if self.are_keys_equal(hash_table_index, key):
                    return hash_table_index

                hash_table_index = self.increase_hash_table_index_by_one(
                    hash_table_index)

        raise KeyError

    def extend_hash_table(self):
        temp_values = self.hash_table.copy()

        self.capacity *= 2
        self.threshold = self.return_threshold()
        self.hash_table = self.setup_hash_table()

        # fill new hash table
        for item in temp_values:
            if item:
                hash_table_index = self.get_hash_table_index_for(item[1])

                while True:
                    if self.is_hash_table_cell_empty(hash_table_index):
                        self.write_to_hash_table(hash_table_index, item)
                        break

                    hash_table_index = self.increase_hash_table_index_by_one(
                        hash_table_index)

    def __init__(self):
        self.capacity = 8
        self.threshold = self.return_threshold()
        self._size = 0
        self.hash_table = self.setup_hash_table()
        self._hash_table_index = None

    def __setitem__(self, key, value):
        key_hash = hash(key)
        item = [key, key_hash, value]
        hash_table_index = self.get_hash_table_index_for(key_hash)

        while True:
            if self.is_hash_table_cell_empty(hash_table_index):
                self.write_to_hash_table(hash_table_index, item)
                self._size += 1
                break

            if self.are_keys_equal(hash_table_index, key):
                self.update_hash_table_value(hash_table_index, item)
                break

            hash_table_index = self.increase_hash_table_index_by_one(
                hash_table_index)

        if self._size == self.threshold:
            self.extend_hash_table()

    def __getitem__(self, key):
        hash_table_index = self.get_hash_table_index_for(hash(key))

        target_cell_hash = self.find_cell_by_hash_and_key(
            hash_table_index, key)

        return self.hash_table[target_cell_hash][2]

    def __len__(self):
        return self._size

    def clear(self):
        self.hash_table = self.setup_hash_table()

    def __delitem__(self, key):
        hash_table_index = self.get_hash_table_index_for(hash(key))

        target_cell_hash = self.find_cell_by_hash_and_key(
            hash_table_index, key)
        self.clear_hash_table_cell(target_cell_hash)
        self._size -= 1

    def get(self, key, default=None):
        hash_table_index = self.get_hash_table_index_for(hash(key))
        try:
            target_cell_hash = self.find_cell_by_hash_and_key(
                hash_table_index, key)

            return self.hash_table[target_cell_hash][2]
        except KeyError:
            return default

    def pop(self, key, default=None):
        hash_table_index = self.get_hash_table_index_for(hash(key))

        try:
            target_cell_hash = self.find_cell_by_hash_and_key(
                hash_table_index, key)

            result = self.hash_table[target_cell_hash][2]
            self.clear_hash_table_cell(target_cell_hash)
            self._size -= 1
            return result
        except KeyError:
            return default

    def __repr__(self):
        result = "{"
        items = []
        for item in self.hash_table:
            if item:
                items.append(f"{item[0]}: {item[2]}")
        result += ", ".join(items) + "}"
        return result
