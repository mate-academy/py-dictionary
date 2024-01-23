from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.bucket = [None] * self.capacity
        self.length = 0

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        try:
            while self.bucket[index] and key != self.bucket[index].key:
                index = (index + 1) % self.capacity
            return self.bucket[index].value
        except AttributeError:
            raise KeyError(f"Dictionary doesn't have a {key} key")

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        try:
            while self.bucket[index] and key != self.bucket[index].key:
                index = (index + 1) % self.capacity
            self.bucket[index] = None
            self.length -= 1
        except AttributeError:
            raise KeyError(f"Dictionary doesn't have a {key} key")

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity

        while self.bucket[index] and self.bucket[index].key != key:
            index = (index + 1) % self.capacity

        if not self.bucket[index]:
            self.length += 1
        self.bucket[index] = Node(key, value)

        if self.length == int(self.capacity * (2 / 3)) + 1:
            self._resize()

    def _resize(self) -> None:
        self.capacity *= 2
        bucket_tmp = [None] * self.capacity
        for element in self.bucket:
            if element:
                index = element.hash % self.capacity
                while bucket_tmp[index]:
                    index = (index + 1) % self.capacity
                bucket_tmp[index] = element
        self.bucket = bucket_tmp

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> iter:
        return iter([(node.key, node.value) for node in self.bucket if node])

    def pop(self, key: Any) -> Any:
        value = self.__getitem__(key)
        self.__delitem__(key)
        return value

    def get(self, key: Any) -> Any:
        return self.__getitem__(key)

    def clear(self) -> None:
        self.capacity = 8
        self.bucket = [None] * self.capacity
