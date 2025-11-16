from typing import Optional


class Structure:
    def __init__(self, key: object, value: object) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.storage: list[Optional[Structure]] = [None] * capacity
        self.size: int = 0

    def _index(self, key: object) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_storage = self.storage
        self.capacity *= 2
        self.storage = [None] * self.capacity
        self.size = 0

        for node in old_storage:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: object, value: object) -> None:
        if self.size >= self.capacity * 0.75:
            self._resize()

        index = self._index(key)

        for _ in range(self.capacity):
            node = self.storage[index]

            if node is None:
                self.storage[index] = Structure(key, value)
                self.size += 1
                return

            if node.key == key:
                node.value = value
                return

            index = (index + 1) % self.capacity

        raise RuntimeError

    def __getitem__(self, key: object) -> object:
        index = self._index(key)

        for _ in range(self.capacity):
            node = self.storage[index]

            if node is None:
                raise KeyError

            if node.key == key:
                return node.value

            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.size
