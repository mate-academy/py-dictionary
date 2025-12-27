from typing import Any, Union, Iterator


class _Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.__initial_capacity = 8
        self.__size = 0
        self.__buckets: list[list[_Node] | None] = [None] * self.__initial_capacity  # O(n)

    def __resize(self) -> None:
        new_capacity = len(self.__buckets) * 2
        new_buckets: list[list[_Node] | None] = [None] * new_capacity

        for bucket in self.__buckets:
            if bucket is not None:
                for node in bucket:
                    new_index = hash(node.key) % new_capacity
                    if new_buckets[new_index] is None:
                        new_buckets[new_index] = []
                    new_buckets[new_index].append(node)

        self.__buckets = new_buckets

    def __setitem__(self, key: Any, value: Any) -> None:
        bucket_index = hash(key) % len(self.__buckets)
        bucket = self.__buckets[bucket_index]

        if bucket is None:
            bucket = []
            self.__buckets[bucket_index] = bucket

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, value))
        self.__size += 1

        if self.__size / len(self.__buckets) > 0.75:
            self.__resize()

    def __getitem__(self, key: Any) -> Any:
        bucket_index = hash(key) % len(self.__buckets)
        bucket = self.__buckets[bucket_index]

        if bucket is not None:
            for node in bucket:
                if node.key == key:
                    return node.value

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.__size

    def __delitem__(self, key: Any) -> None:
        bucket_index = hash(key) % len(self.__buckets)
        bucket = self.__buckets[bucket_index]

        if bucket is not None:
            for i, node in enumerate(bucket):
                if node.key == key:
                    bucket.pop(i)
                    self.__size -= 1
                    return

        raise KeyError(f"Key {key} not found")

    def get(self, key: Any, default: Any = None) -> Any:
        bucket_index = hash(key) % len(self.__buckets)
        bucket = self.__buckets[bucket_index]

        if bucket is not None:
            for node in bucket:
                if node.key == key:
                    return node.value

        return default

    def pop(self, key: Any, default: Any = None) -> Any:
        bucket_index = hash(key) % len(self.__buckets)
        bucket = self.__buckets[bucket_index]

        if bucket is not None:
            for i, node in enumerate(bucket):
                if node.key == key:
                    self.__size -= 1
                    return bucket.pop(i).value

        if default is not None:
            return default

        raise KeyError(f"Key {key} not found")

    def update(self, other: Union[dict, "Dictionary"]) -> None:
        if isinstance(other, Dictionary):
            for bucket in other.__buckets:
                if bucket is not None:
                    for node in bucket:
                        self[node.key] = node.value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            raise TypeError("Argument must be of type dict or Dictionary")

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.__buckets:
            if bucket is not None:
                for node in bucket:
                    yield node.key
