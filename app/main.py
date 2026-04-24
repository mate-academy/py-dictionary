from typing import Any


_DELETED = object()

class DictionaryNode:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(self.key)

class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity
        self.threshold = 2 / 3

    def index(self, hash_key: Any) -> int:
        return hash_key % self.capacity

    def size_threshold(self) -> None:
        if round(self.capacity * self.threshold) == self.size:
            temp_nodes_storage = [node for node in self.table if node is not None and node is not _DELETED]
            self.capacity *= 2
            self.table = [None] * self.capacity
            self.size = 0
            for node in temp_nodes_storage:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        self.size_threshold()
        new_dict = DictionaryNode(key, value)
        index = self.index(new_dict.hash_key)

        while (
                self.table[index] is not None and
                self.table[index].key != key and
                self.table[index] is not _DELETED):
            index = (index + 1) % self.capacity

        if self.table[index] is None:
            self.size += 1

        self.table[index] = new_dict

    def __getitem__(self, key: Any) -> Any:
        index = self.index(hash(key))
        counter = 0

        while self.table[index] is not None:
            if counter > self.capacity:
                raise KeyError
            if self.table[index].key is not _DELETED and self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
            counter += 1

        raise KeyError

    def __delitem__(self, key: Any) -> None:
        index = self.index(hash(key))

        while self.table[index] is not None:
            if self.table[index] is not _DELETED and self.table[index].key == key:
                self.table[index] = _DELETED
                self.size -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.size
