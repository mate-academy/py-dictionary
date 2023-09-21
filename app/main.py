from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, new_hash: int, value: str) -> None:
        self.key = key
        self.value = value
        self.hash = new_hash

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3

    ) -> None:

        self.capacity: int = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self._hash_list = [None] * self.capacity

    def find_slot(self, key: Hashable) -> int:
        new_hash = hash(key)
        index = new_hash % self.capacity
        while self._hash_list[index]:
            if self._hash_list[index].key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        self.capacity *= 2
        old_hash_list = self._hash_list
        self._hash_list = [None] * self.capacity
        self.size = 0

        for item in old_hash_list:
            if item:
                self.__setitem__(item.key, item.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        new_hash = hash(key)
        index = self.find_slot(key)
        if self._hash_list[index] is None:
            self.size += 1

        self._hash_list[index] = Node(key, new_hash, value)

        if self.size >= self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> str:
        index = self.find_slot(key)
        if self._hash_list[index]:
            return self._hash_list[index].value
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.size = 0
        self._hash_list = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self.find_slot(key)
        if self._hash_list[index]:
            self._hash_list[index].value = None
            self.size -= 1
        else:
            raise KeyError(f"Key for deleting is not found: {key}")

    def pop(self, key: Hashable, default_value: Any = None) -> object:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default_value:
                return default_value
            raise
