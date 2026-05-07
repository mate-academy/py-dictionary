from typing import Any


class Dictionary:
    TOMBSTONE = object()

    def __init__(
            self,
            initial_capacity: int = 8
    ) -> None:
        self.initial_capacity = initial_capacity
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def __setitem__(
            self,
            key : Any,
            value : Any
    ) -> None:
        node = Node(key, value)
        if self.size + 1 > self.capacity * 2 / 3:
            self._enlarge()
        index = self._key_index(key)
        counter = 0
        while (self.buckets[index] is not None
               and self.buckets[index] is not Dictionary.TOMBSTONE
               and self.buckets[index].key != key):
            if counter > self.capacity:
                break
            index += 1
            index %= self.capacity
            counter += 1
        if self.buckets[index] is None:
            self.size += 1
        self.buckets[index] = node

    def __getitem__(
            self,
            key: Any
    ) -> Any:
        index = self._key_index(key)
        counter = 0
        while (self.buckets[index] is not None
               and self.buckets[index] is not Dictionary.TOMBSTONE):
            if counter > self.capacity:
                break
            if self.buckets[index].key == key:
                return self.buckets[index].value
            index += 1
            index %= self.capacity
            counter += 1
        raise KeyError(f"There is not {key} in the dictionary")

    def __len__(
            self
    ) -> int:
        return self.size

    def _key_index(
            self,
            key : Any
    ) -> int:
        return hash(key) % self.capacity

    def __delitem__(
            self,
            key: Any
    ) -> None:
        index = self._key_index(key)
        counter = 0
        while (self.buckets[index] is not None
               and self.buckets[index] is not Dictionary.TOMBSTONE):
            if counter > self.capacity:
                break
            if self.buckets[index].key == key:
                self.buckets[index] = Dictionary.TOMBSTONE
                self.size -= 1
                break
            index += 1
            index %= self.capacity
            counter += 1

    def _enlarge(
            self
    ) -> None:
        bucket_copy = self.buckets.copy()
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for node in bucket_copy:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def clear(
            self
    ) -> None:
        self.capacity = self.initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def get(
            self,
            key: Any,
            default: Any = None
    ) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(
            self,
            key: Any
    ) -> Any:
        value = self.__getitem__(key)
        self.__delitem__(key)
        return value

    def update(
            self,
            key_values: iter
    ) -> None:
        if hasattr(key_values, "items"):
            key_values = key_values.items()
        for key, value in key_values:
            self.__setitem__(key, value)

    def __iter__(
            self
    ) -> Any:
        for node in self.buckets:
            if node is not None and node is not Dictionary.TOMBSTONE:
                yield node.key


class Node:
    def __init__(
            self,
            key: Any,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __str__(
            self
    ) -> str:
        return f"Node({self.key}, {self.value})"

    def __repr__(
            self
    ) -> str:
        return f"Node({self.key}, {self.value})"
