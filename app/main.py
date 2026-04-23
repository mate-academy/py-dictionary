from typing import Any, Optional, Iterator


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = key_hash
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.load_factor: float = 0.75

    def _get_index(self, key: Any) -> tuple[int, int]:
        key_hash: int = hash(key)
        index: int = key_hash % self.capacity
        return key_hash, index

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for node in old_table:
            current = node
            while current:
                self.put(current.key, current.value)
                current = current.next

    def put(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        key_hash, index = self._get_index(key)
        current = self.table[index]
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        new_node = Node(key, value, key_hash)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

    def get_node(self, key: Any) -> Optional[Node]:
        _, index = self._get_index(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    def get(self, key: Any, default: Any = None) -> Any:
        node = self.get_node(key)
        return node.value if node else default

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __getitem__(self, key: Any) -> Any:
        node = self.get_node(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: Any) -> bool:
        return self.get_node(key) is not None

    def pop(self, key: Any, default: Any = None) -> Any:
        key_hash, index = self._get_index(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                self.size -= 1
                return current.value
            prev = current
            current = current.next
        if default is not None:
            return default
        raise KeyError(key)

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def update(self, other: Any) -> None:
        if hasattr(other, "items") and callable(other.items):
            for k, v in other.items():
                self.put(k, v)
        else:
            for k, v in other:
                self.put(k, v)

    def __iter__(self) -> Iterator[Any]:
        for current in self.table:
            while current:
                yield current.key
                current = current.next

    def __delitem__(self, key: Any) -> None:
        key_hash, index = self._get_index(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next

                self.size -= 1
                return

            prev = current
            current = current.next

        raise KeyError(key)
