from typing import Any, Tuple, Optional


class Node:

    def __init__(self, key: Any, value: Any, h: int) -> None:
        self.key = key
        self.value = value
        self.hash = h


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.75
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _index_for(self, h: int) -> int:
        return h % self.capacity

    def _find_node(self, key: Any, h: int) -> Tuple[Optional[Node], int]:
        index = self._index_for(h)
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.hash == h and node.key == key:
                return node, i
        return None, -1

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        node, _ = self._find_node(key, h)

        if node:
            return node.value
        else:
            raise KeyError(f"Key not found: {key}")

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        index = self._index_for(h)
        bucket = self.buckets[index]
        node, _ = self._find_node(key, h)

        if node:
            node.value = value
            return
        new_node = Node(key, value, h)
        bucket.append(new_node)
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> Any:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self.__setitem__(node.key, node.value)
