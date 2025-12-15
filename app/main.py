from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:

    def __init__(self) -> None:
        self.__capacity = 8
        self.__length = 0
        self.__hash_table = [None] * self.__capacity
        self.__load_factor = 2 / 3

    def __len__(self) -> int:
        return self.__length

    def __setitem__(self, key: Any, value: Any) -> None:
        node = Node(key, value)
        index = node.hash % self.__capacity
        if self.__hash_table[index] is None:
            self.__hash_table[index] = node
            self.__length += 1
        else:
            if self.__hash_table[index].key != key:
                for i in range(1, self.__capacity):
                    new_index = (index + i) % self.__capacity
                    if self.__hash_table[new_index] is None:
                        self.__length += 1
                        break
                    if self.__hash_table[new_index].key == key:
                        break

                self.__hash_table[new_index] = node
            else:
                self.__hash_table[index] = node

        if self.__length >= self.__load_factor * self.__capacity:
            self.__resize()

    @staticmethod
    def find_bucket(hash_table: list, index: int, capacity: int) -> int:
        i = 1
        while True:
            next_index = (index + i) % capacity
            if hash_table[next_index] is None:
                return next_index
            i += 1

    def __resize(self) -> None:
        new_capacity = self.__capacity * 2

        new_hash_table = [None] * new_capacity
        for node in self.__hash_table:
            if node is not None:
                new_index = node.hash % new_capacity
                if new_hash_table[new_index] is not None:
                    new_index = Dictionary.find_bucket(
                        new_hash_table, new_index, new_capacity)
                new_hash_table[new_index] = node

        self.__hash_table = new_hash_table
        self.__capacity = new_capacity

    def __getitem__(self, key: Any) -> Any | None:
        index = self.__find_index_of_element(key)
        return self.__hash_table[index].value

    def __delitem__(self, key: Any) -> None:
        index = self.__find_index_of_element(key)
        self.__hash_table[index] = None
        self.__length -= 1

    def __find_index_of_element(self, key: Any) -> int:
        _hash = hash(key)
        index = _hash % self.__capacity
        if self.__hash_table[index] is None:
            raise KeyError(f"Key {key} not found!")
        if self.__hash_table[index].key != key:
            for i in range(1, self.__capacity):
                new_index = (index + i) % self.__capacity
                if self.__hash_table[new_index] is None:
                    raise KeyError(f"Key {key} not found!")
                if self.__hash_table[new_index].key == key:
                    break
            return new_index
        return index

    def clear(self) -> None:
        self.__hash_table = [None] * self.__capacity
        self.__length = 0

    def get(self, key: Any, default: None) -> Any | None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
