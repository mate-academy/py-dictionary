from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.dict_size = 0
        self._hash_table = [None] * self.capacity

    def __hash_index__(self, key_hash: int) -> None:
        return key_hash % self.capacity

    def __resize__(self) -> None:
        old_table = self._hash_table
        self.capacity *= 2
        self._hash_table = [None] * self.capacity
        self.dict_size = 0

        for item in old_table:
            if item:
                for key, key_hash, value in item:
                    self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self.__hash_index__(key_hash)

        if self._hash_table[index] is None:
            self._hash_table[index] = []

        found = False
        for i, (item_key, item_hash, _) in enumerate(self._hash_table[index]):
            if item_key == key:
                self._hash_table[index][i] = (key, key_hash, value)
                found = True
                break

        if not found:
            self._hash_table[index].append((key, key_hash, value))
            self.dict_size += 1

        if self.dict_size / self.capacity > 0.75:
            self.__resize__()

    def __getitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self.__hash_index__(key_hash)
        if self._hash_table[index] is None:
            raise KeyError(key)

        for other_key, key_hash, value in self._hash_table[index]:
            if other_key == key:
                return value

        raise KeyError(key)

    def __len__(self) -> None:
        return self.dict_size

    def clear(self) -> None:
        self._hash_table = [None] * self.capacity
        self.dict_size = 0

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self.__hash_index__(key_hash)

        if self._hash_table[index] is None:
            raise KeyError(key)

        for i, (other_key, key_hash, value) in enumerate(
                self._hash_table[index]
        ):
            if other_key == key:
                del self._hash_table[index][i]
                self.dict_size -= 1
                return

        raise KeyError(key)

    def get(self, key: Hashable, default: Any) -> None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any) -> None:
        key_hash = hash(key)
        index = self.__hash_index__(key_hash)

        if self._hash_table[index] is None:
            if default is not None:
                return default
            else:
                raise KeyError(key)

        for i, (other_key, key_hash, value) in enumerate(
                self._hash_table[index]
        ):
            if other_key == key:
                self.dict_size -= 1
                return self._hash_table[index].pop(i)[2]

        if default is not None:
            return default
        else:
            raise KeyError(key)

    def update(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setitem__(key, value)

        for arg in args:
            if isinstance(arg, dict) or isinstance(arg, Dictionary):
                for key, value in arg.items():
                    self.__setitem__(key, value)
            else:
                try:
                    for key, value in arg:
                        self.__setitem__(key, value)
                except TypeError:
                    raise ValueError(
                        "Argument must be a dictionary-like object"
                    )

    def __iter__(self) -> None:
        for bucket in self._hash_table:
            if bucket:
                for key, _, _ in bucket:
                    yield key
