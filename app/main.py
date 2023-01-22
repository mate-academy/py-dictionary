from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.nodes = [[] for i in range(self.capacity)]
        self.old_nodes = None

    @property
    def threshold(self) -> int:
        return int(self.capacity * 2 / 3)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size == self.threshold:
            self.resize_dict()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if not self.nodes[index]:
                self.nodes[index].extend([key, hashed_key, value])
                self.size += 1
                break
            if self.nodes[index][0] == key:
                self.nodes[index] = [key, hashed_key, value]
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if not self.nodes[index]:
                raise KeyError
            if self.nodes[index][0] == key:
                return self.nodes[index][2]
            index = (index + 1) % self.capacity

    def resize_dict(self) -> None:
        self.capacity *= 2
        self.size = 0
        self.old_nodes = self.nodes
        self.nodes = [[] for i in range(self.capacity)]
        for element in self.old_nodes:
            if element:
                self.__setitem__(
                    key=element[0],
                    value=element[2]
                )

    def __len__(self) -> int:
        return self.size
