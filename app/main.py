from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable ,
            value: Any,
            key_hash: int
    ) -> None:
        self.key = key
        self.value = value
        self.key_hash = key_hash


class Dictionary:
    default_capacity = 8
    max_load_factor = 0.75

    def __init__(self) -> None:
        self._table = [[] for _ in range(self.default_capacity)]
        self._capacity = self.default_capacity
        self._size = 0

    def get_bucket_index(self, key_hash: int) -> int:
        return key_hash & (self._capacity - 1)

    def setitem_no_resize(
            self, key: Hashable,
            value: Any,
            key_hash: int
    ) -> None:
        index = self.get_bucket_index(key_hash)
        bucket = self._table[index]
        for node in bucket:
            if node.key_hash == key_hash and node.key == key:
                node.value = value
                return

        new_node = Node(key, value, key_hash)
        bucket.append(new_node)
        self._size += 1

    def resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_table:
            for node in bucket:
                self.setitem_no_resize(node.key, node.value, node.key_hash)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self.get_bucket_index(key_hash)
        bucket = self._table[index]
        is_updated = False
        for node in bucket:
            if node.key == key and node.key_hash == key_hash:
                is_updated = True
                break
        if not is_updated and (
                (self._size + 1) > self._capacity * self.max_load_factor
        ):
            self.resize()

        self.setitem_no_resize(key, value, key_hash)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self.get_bucket_index(key_hash)
        bucket = self._table[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._table = [[] for _ in range(self.default_capacity)]
        self._capacity = self.default_capacity
        self._size = 0

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self.get_bucket_index(key_hash)
        bucket = self._table[index]

        for i, node in enumerate(bucket):
            if node.key_hash == key_hash and node.key == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)
