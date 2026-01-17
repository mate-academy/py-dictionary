from collections import namedtuple
from typing import Any

Node = namedtuple("Node", "key, value, hash_code")


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.length = 0
        self._table: list[None | Node] = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_code = hash(key)
        index = hash_code % self.capacity
        for _ in range(self.capacity):
            node = self._table[index]
            if node is None:
                self._table[index] = Node(key, value, hash_code)
                self.length += 1
                if self.length > self.capacity * self.load_factor:
                    self.resize()
                break
            if node.hash_code == hash_code and node.key == key:
                self._table[index] = Node(key, value, hash_code)
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        hash_code = hash(key)
        index = hash_code % self.capacity
        for _ in range(self.capacity):
            node = self._table[index]
            if node is None:
                raise KeyError(key)
            if node.hash_code == hash_code and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_code = hash(key)
        index = hash_code % self.capacity
        for _ in range(self.capacity):
            node = self._table[index]
            if node is None:
                raise KeyError(key)
            if node.hash_code == hash_code and node.key == key:
                self._table[index] = None
                self.length -= 1
                break

    def __iter__(self) -> Any:
        yield from self.nodes

    def __str__(self) -> str:
        nodes = []
        for node in self.nodes:
            nodes.append(f"{node.key!r}: {node.value!r}")
        return f"{{{', '.join(nodes)}}}"

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def pop(self, key: Any, default: Any = None) -> Any:
        if key not in self:
            if not default:
                raise KeyError(key)
            return default
        item = self[key]
        del self[key]
        return item

    def update(self, dictionary: dict) -> None:
        for key, value in dictionary.items():
            self[key] = value

    def resize(self) -> None:
        copy = Dictionary(capacity=self.capacity * 2)
        for node in self:
            copy[node.key] = node.value
        self._table = copy._table
        self.capacity = copy.capacity

    def clear(self) -> None:
        for i in range(self.capacity):
            self._table[i] = None
            self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    @property
    def nodes(self) -> set:
        return {node for node in self._table if node}

    @property
    def keys(self) -> set:
        return {node.key for node in self._table if node}

    @property
    def values(self) -> list:
        return [node.value for node in self._table if node]
