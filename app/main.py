from typing import Any, Hashable


class Node:
    def __init__(self, hash_key: int, key: Hashable, value: Any) -> None:
        self.hash_key = hash_key
        self.key = key
        self.value = value


class DeletedMarker:
    pass


class Dictionary:

    def __init__(self) -> None:
        self._capacity = 8
        self._size_dict = 0
        self.hash_cell = [None] * self._capacity
        self.load_memory = 0.667

    def clear(self) -> None:
        self.hash_cell = [None] * self._capacity
        self._size_dict = 0

    def get_hash(self, key: Hashable) -> int:
        hash_key = hash(key) % self._capacity
        while (self.hash_cell[hash_key] not in [None, DeletedMarker]
               and self.hash_cell[hash_key].key != key):
            hash_key = (hash_key + 1) % self._capacity
        return hash_key

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = self.get_hash(key)
        if self.hash_cell[hash_key] is None:
            self._size_dict += 1
            self.hash_cell[hash_key] = Node(hash(key), key, value)
        else:
            self.hash_cell[hash_key].value = value
        if self._size_dict > self._capacity * self.load_memory:
            self._resize()

    def update(self, new_dict: dict) -> None:
        for key, value in new_dict.items():
            self[key] = value

    def __delitem__(self, key: Hashable) -> None:
        key_hash = self.get_hash(key)
        if (self.hash_cell[key_hash] and self.hash_cell[key_hash].key == key):
            self.hash_cell[key_hash] = Node(None, DeletedMarker, None)
            self._size_dict -= 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = self.get_hash(key)
        if self.hash_cell[hash_key] is None:
            raise KeyError("key does not exist")
        return self.hash_cell[hash_key].value

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def _resize(self) -> None:
        temporaries = self.hash_cell
        self._capacity *= 2
        self.clear()
        for node in temporaries:
            if node and node.key not in [None, DeletedMarker]:
                self[node.key] = node.value

    def __len__(self) -> int:
        return self._size_dict

    def __repr__(self) -> str:
        all_dict = ", ".join(f"{node.key}: {node.value}"
                             for node in self.hash_cell if node)
        return f"{{{all_dict}}}"
