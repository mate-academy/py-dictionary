from dataclasses import dataclass
from typing import Any, Optional, Iterator, Iterable, Tuple


@dataclass(slots=True)
class _Node:
    key: Any
    key_hash: int
    value: Any
    next_node: Optional["_Node"] = None


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 max_load: float = 0.75
                 ) -> None:
        if initial_capacity < 1:
            raise ValueError("Initial capacity must be >= 1")
        capacity_power_of_two = 1
        while capacity_power_of_two < initial_capacity:
            capacity_power_of_two <<= 1
        self._buckets = [None] * capacity_power_of_two
        self._size = 0
        self._max_load = float(max_load)

    @property
    def _capacity(self) -> int:
        return len(self._buckets)

    def _bucket_index_for_hash(self, key_hash: int) -> int:
        return key_hash & (self._capacity - 1)

    def _maybe_resize(self) -> None:
        if (self._size / self._capacity) > self._max_load:
            self._resize(self._capacity << 1)

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        capacity_power_of_two = 1
        while capacity_power_of_two < new_capacity:
            capacity_power_of_two <<= 1
        self._buckets = [None] * capacity_power_of_two

        for head_node in old_buckets:
            current_node = head_node
            while current_node is not None:
                next_in_chain = current_node.next_node
                bucket_index = self._bucket_index_for_hash(
                    current_node.key_hash
                )
                current_node.next_node = self._buckets[bucket_index]
                self._buckets[bucket_index] = current_node
                current_node = next_in_chain

    def _find_in_bucket(self,
                        key: Any,
                        key_hash: int,
                        bucket_index: int
                        ) -> tuple:
        previous_node = None
        current_node = self._buckets[bucket_index]
        while current_node is not None:
            if current_node.key_hash == key_hash and current_node.key == key:
                return previous_node, current_node
            previous_node = current_node
            current_node = current_node.next_node
        return None, None

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        bucket_index = self._bucket_index_for_hash(key_hash)
        previous_node, found_node = self._find_in_bucket(
            key, key_hash, bucket_index
        )

        if found_node is not None:
            found_node.value = value
            return

        new_node = _Node(
            key=key,
            key_hash=key_hash,
            value=value,
            next_node=self._buckets[bucket_index],
        )
        self._buckets[bucket_index] = new_node
        self._size += 1
        self._maybe_resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        bucket_index = self._bucket_index_for_hash(key_hash)
        _, found_node = self._find_in_bucket(key, key_hash, bucket_index)
        if found_node is None:
            raise KeyError(f"Key {key!r} not found")
        return found_node.value

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for head_node in self._buckets:
            current_node = head_node
            while current_node is not None:
                yield current_node.key
                current_node = current_node.next_node

    def items(self) -> Iterator[Tuple[Any, Any]]:
        for head_node in self._buckets:
            current_node = head_node
            while current_node is not None:
                yield (current_node.key, current_node.value)
                current_node = current_node.next_node

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        bucket_index = self._bucket_index_for_hash(key_hash)
        previous_node, node = self._find_in_bucket(key, key_hash, bucket_index)
        if node is None:
            raise KeyError(f"Key {key!r} not found")

        # remove node from linked list
        if previous_node is None:
            self._buckets[bucket_index] = node.next_node
        else:
            previous_node.next_node = node.next_node
        self._size -= 1

    def get(self, key: Any, default: Any = None) -> Any:
        key_hash = hash(key)
        bucket_index = self._bucket_index_for_hash(key_hash)
        _, node = self._find_in_bucket(key, key_hash, bucket_index)
        return node.value if node is not None else default

    def pop(self, key: Any, default: Any = ...) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is ...:
                raise
            return default
        else:
            del self[key]
            return value

    def update(
        self, other: Optional[Iterable[Tuple[Any, Any]]] = None, **kwargs: Any
    ) -> None:
        if other is not None:
            if isinstance(other, Dictionary):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value
