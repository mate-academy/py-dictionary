from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any, hash_code: int) -> None:
        self.key = key
        self.value = value
        self.hash_code = hash_code
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.__initial_capacity = 16
        self.__load_factor = 0.75
        self.capacity = self.__initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) & 0x7FFFFFFF

    def _resize(self, new_capacity: int) -> None:
        old_table = self.table
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def _should_resize(self) -> bool:
        return self.size >= self.capacity * self.__load_factor

    def _get_node(self, key: Hashable, hash_code: int) -> Node:
        index = hash_code % self.capacity
        node = self.table[index]

        while node:
            if node.hash_code == hash_code and node.key == key:
                return node
            node = node.next

        return None

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_code = self._hash(key)
        index = hash_code % self.capacity

        existing_node = self._get_node(key, hash_code)
        if existing_node:
            existing_node.value = value
        else:
            new_node = Node(key, value, hash_code)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

        if self._should_resize():
            self._resize(self.capacity * 2)

    def __getitem__(self, key: Hashable) -> Any:
        hash_code = self._hash(key)
        node = self._get_node(key, hash_code)

        if node:
            return node.value
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        hash_code = self._hash(key)
        index = hash_code % self.capacity
        node = self.table[index]
        prev = None

        while node:
            if node.hash_code == hash_code and node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.size -= 1
                return

            prev = node
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Any:
        for node in self.table:
            while node:
                yield node.key
                node = node.next

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.capacity = 16
        self.size = 0
        self.table = [None] * self.capacity

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __repr__(self) -> str:
        items = [f"{key}: {value}" for key, value in self.items()]
        return "{" + ", ".join(items) + "}"
