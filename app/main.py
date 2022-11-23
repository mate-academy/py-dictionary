from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.current_size = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.load_factor)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.current_size == self.threshold:
            self._resize()
        node = [key, value, hash(key)]
        index_from_hash = hash(key) % self.capacity

        if not self.hash_table[index_from_hash]:
            self.hash_table[index_from_hash] = node
            self.current_size += 1
            return

        for i in self.hash_table:
            if i:
                if i[0] == key:
                    current_index = self.hash_table.index(i)
                    self.hash_table[current_index] = node
                    return

        for index in range(index_from_hash + 1, len(self.hash_table)):
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.current_size += 1
                return

        for index in range(0, index_from_hash):
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.current_size += 1
                return

    def __getitem__(self, key: Hashable) -> Any:
        hashed_value = hash(key)
        current_index = hashed_value % self.capacity
        current_element = self.hash_table[current_index]

        while current_element:
            if current_element[2] == hashed_value \
                    and current_element[0] == key:
                return current_element[1]
            current_index = (current_index + 1) % self.capacity
            current_element = self.hash_table[current_index]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.current_size

    def _resize(self) -> None:
        self.capacity *= 2
        self.current_size = 0
        self.threshold = int(self.capacity * self.load_factor)
        self.old_hash_table = self.hash_table[::]
        self.hash_table = [[] for _ in range(self.capacity)]
        for element in self.old_hash_table:
            if element:
                self.__setitem__(element[0], element[1])
        self.old_hash_table = None
