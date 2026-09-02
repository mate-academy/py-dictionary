from typing import Any, Iterable


class Dictionary:

    def __init__(self, items: Iterable = None) -> None:
        self.__table_size = 8
        self.__table = [[] for _ in range(self.__table_size)]
        self.__items_size = 0
        if items:
            self.update(items)

    def _hash_key(self, key: Any) -> int:
        return hash(key) % self.__table_size

    def _rearrange_table_size(self) -> None:
        if self.__items_size > (2 / 3) * self.__table_size:
            self.__table_size *= 2
            old_table = self.__table
            self.__table = [[] for _ in range(self.__table_size)]

            for bucket in old_table:
                for key_hash, key, value in bucket:
                    bucket_index = key_hash % self.__table_size
                    self.__table[bucket_index].append([key_hash, key, value])

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        bucket_index = key_hash % self.__table_size
        bucket = self.__table[bucket_index]

        for item in bucket:
            if item[0] == key_hash and item[1] == key:
                item[2] = value
                return

        bucket.append([key_hash, key, value])
        self.__items_size += 1
        self._rearrange_table_size()

    def __getitem__(self, key: str) -> Any:
        key_hash = hash(key)
        bucket = self.__table[key_hash % self.__table_size]

        for item_hash, item_key, item_value in bucket:
            if item_hash == key_hash and item_key == key:
                return item_value

        raise KeyError(f"{key} not in map")

    def __len__(self) -> int:
        return self.__items_size

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        bucket = self.__table[key_hash % self.__table_size]

        for index, (item_hash, item_key, item_value) in enumerate(bucket):
            if item_hash == key_hash and item_key == key:
                bucket.pop(index)
                self.__items_size -= 1
                return

        raise KeyError(f"{key} not in map")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        popped_item = self.__getitem__(key)
        self.__delitem__(key)
        return popped_item

    def update(self, iter_value: Any) -> None:
        if isinstance(iter_value, dict):
            iterable = iter_value.items()
        else:
            iterable = iter(iter_value)

        try:
            for key, value in iterable:
                self.__setitem__(key, value)
        except (TypeError, ValueError):
            raise TypeError(f"{iter_value} is not iterable of pairs")

    def items(self) -> Iterable[Any]:
        for bucket in self.__table:
            for item_hash, key, value in bucket:
                yield key, value

    def values(self) -> Iterable[Any]:
        for bucket in self.__table:
            for item_hash, key, value in bucket:
                yield value

    def keys(self) -> Iterable[Any]:
        return self.__iter__()

    def __iter__(self) -> Iterable[Any]:
        for bucket in self.__table:
            for item_hash, key, value in bucket:
                yield key
