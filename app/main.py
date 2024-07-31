from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.nodes = [(0, 0, 0)] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.capacity * self.load_factor:
            self.resize()
        key_hash = hash(key)
        key_index = self.get_index(key)

        if key != self.nodes[key_index][0]:
            self.size += 1
        self.nodes[key_index] = (key, key_hash, value)

    def __getitem__(self, key: Hashable) -> Any:
        key_index = self.get_index(key)
        if not any(self.nodes[key_index]):
            raise KeyError
        return self.nodes[key_index][2]

    def __len__(self) -> int:
        return self.size

    def get_index(
            self,
            key: Hashable
    ) -> int:
        key_hash = hash(key)
        key_index = key_hash % self.capacity

        while any(self.nodes[key_index]):

            if key == self.nodes[key_index][0]:
                return key_index

            key_index = (key_index + 1) % self.capacity

        return key_index

    def resize(self) -> None:
        self.capacity *= 2

        old_nodes = self.nodes.copy()

        self.nodes = [(0, 0, 0)] * self.capacity
        for node in old_nodes:
            key_index = self.get_index(node[0])
            self.nodes[key_index] = node

    def clear(self) -> None:
        self.nodes = [(0, 0, 0)] * self.capacity
        self.size = 0

    def __iter__(self) -> Any:
        for node in self.nodes:
            if node[0] is not None:
                yield node[0]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __delitem__(self, key: Hashable) -> None:
        key_index = self.get_index(key)
        if self.nodes[key_index][0] is None:
            raise KeyError(key)

        self.nodes[key_index] = (None, None, None)
        self.size -= 1

    def update(self, other: Any = None, **kwargs) -> None:
        if other is not None:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self.__setitem__(key, other[key])
            else:
                for key, value in other:
                    self.__setitem__(key, value)
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def pop(self, key: Hashable, default: Any = None) -> None:
        key_index = self.get_index(key)
        if self.nodes[key_index][0] is None:
            if default is not None:
                return default
            raise KeyError(key)

        self.__delitem__(key)
