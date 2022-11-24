class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.index_set: set = set()
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def get_index(self, key: object) -> int:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if key == self.hash_table[index][0]:
                break
            if index == self.capacity - 1:
                index = 0
            else:
                index += 1
        return index

    def resize_hash_table(self) -> None:
        old_hash_table = self.hash_table.copy()
        old_index_set = self.index_set.copy()
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.index_set.clear()

        for old_index in old_index_set:
            key, value = old_hash_table[old_index]
            index = self.get_index(key)
            self.hash_table[index] = (key, value)
            self.index_set.add(index)

    def __setitem__(self, key: object, value: object) -> None:
        if self.length == round(self.capacity * 2 / 3):
            self.resize_hash_table()

        index = self.get_index(key)
        self.hash_table[index] = (key, value)
        if index not in self.index_set:
            self.index_set.add(index)
            self.length += 1

    def __getitem__(self, item: object) -> object:
        index = self.get_index(item)
        if self.hash_table[index] is not None:
            return self.hash_table[index][1]
        raise KeyError(f"Key {item} not found")

    def get_value_index(self, key: object) -> tuple:
        index = self.get_index(key)
        hash_value = self.hash_table[index]
        if hash_value is not None:
            return hash_value[1], index
        return None, index

    def __delitem__(self, key: object) -> object:
        hash_value, index = self.get_value_index(key)
        if hash_value is not None:
            self.hash_table[index] = None
            self.index_set.remove(index)
            self.length -= 1
            return hash_value
        return None

    def clear(self) -> None:
        self.__init__()

    def pop(self, key: object) -> object:
        return self.__delitem__(key)

    def get(self, key: object) -> object:
        hash_value, _ = self.get_value_index(key)
        return hash_value
