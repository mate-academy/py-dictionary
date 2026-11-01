from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.ls = [None] * self.size
        self.count = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.size

        while self.ls[index] is not None:
            node = self.ls[index]

            if node.hash == key_hash and (node.key is key or node.key == key):
                node.value = value
                return

            index = (index + 1) % self.size

        if (self.count + 1) / self.size > 2 / 3:
            self._resize()
            self[key] = value
            return

        self.ls[index] = Node(key, value)
        self.count += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.size

        while self.ls[index] is not None:
            node = self.ls[index]

            if node.hash == key_hash and (node.key is key or node.key == key):
                return node.value

            index = (index + 1) % self.size

        raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        old_list = self.ls

        self.size *= 2
        self.ls = [None] * self.size
        self.count = 0

        for node in old_list:
            if node is not None:
                self[node.key] = node.value
