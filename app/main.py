from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.count = 0
        self.DELETED = object()

    def _resize_threshold(self) -> int:
        return round(len(self.hash_table) * (2 / 3))

    def _find_index(self, hash_table: list[Any], hash_: int, key: Any) -> int:
        index_ = hash_ % len(hash_table)
        for _ in range(len(hash_table)):
            entry = hash_table[index_]
            if (
                    entry is None or entry is self.DELETED or (
                    entry["hash_key"] == hash_ and entry["key"] == key)
            ):
                return index_
            index_ = (index_ + 1) % len(hash_table)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        hash_data = {"key": key, "value": value, "hash_key": hash_key}

        if self.__len__() == self._resize_threshold():
            new_hash_table = [None] * (len(self.hash_table) * 2)
            for x in self.hash_table:
                if x is not None and x is not self.DELETED:
                    index_new_hash_table = (
                        self._find_index(
                            new_hash_table, x["hash_key"], x["key"]
                        )
                    )
                    new_hash_table[index_new_hash_table] = x
            self.hash_table = new_hash_table

        index = self._find_index(self.hash_table, hash_key, key)
        entry = self.hash_table[index]
        if entry is None or entry is self.DELETED:
            self.count += 1
        self.hash_table[index] = hash_data

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = self._find_index(self.hash_table, hash_key, key)
        entry = self.hash_table[index]
        if (
                entry is not None
                and entry is not self.DELETED
                and entry["key"] == key
        ):
            return entry["value"]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.count = 0

    def __delitem__(self, key: Any) -> None:
        def find_index_for_del(hash_: int) -> int:
            index_ = hash_ % len(self.hash_table)
            for _ in range(len(self.hash_table)):
                entry = self.hash_table[index_]
                if entry is None:
                    break
                if (
                        entry is not self.DELETED
                        and entry["hash_key"] == hash_
                        and entry["key"] == key
                ):
                    return index_
                index_ = (index_ + 1) % len(self.hash_table)
            raise KeyError(key)

        hash_key = hash(key)
        index = find_index_for_del(hash_key)
        entry = self.hash_table[index]

        if entry["key"] == key:
            self.hash_table[index] = self.DELETED
            self.count -= 1

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is None:
                raise KeyError(key)
            return default

    def update(self, *args, **kwargs) -> None:
        if args:
            for item in args:
                if isinstance(item, dict):
                    for key, value in item.items():
                        self.__setitem__(key, value)
                else:
                    for it in item:
                        if len(it) == 2:
                            key, value = it[0], it[1]
                            self.__setitem__(key, value)
                        else:
                            raise ValueError(it)
        if kwargs:
            for key, value in kwargs.items():
                self.__setitem__(key, value)

    def __iter__(self) -> Any:
        for item in self.hash_table:
            if item is not None and item is not self.DELETED:
                yield item["key"]
