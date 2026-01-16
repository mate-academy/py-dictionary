from typing import Any, Hashable


class Dictionary:
    def __init__(self, **kwargs) -> None:
        self.hash_table = [-1] * 8
        self.dictionary = []
        self.length = 0
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, list | dict | set):
            raise TypeError(f"<{key}> cannot be a dictionary key")

        if len(self.dictionary) >= int(self.get_load_factor()):
            self.resize()

        hash_code = hash(key)
        hash_index, dict_index = self.set_index(hash_code, key)
        if dict_index == -1:
            self.hash_table[hash_index] = len(self.dictionary)
            self.dictionary.append((hash_code, key, value))
            self.length += 1
        else:
            self.dictionary[dict_index] = (hash_code, key, value)

    def __getitem__(self, key: Hashable) -> Any:
        return self.dictionary[self.get_index(key)[-1]][-1]

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def update(self, items: dict | list | tuple) -> None:
        if not isinstance(items, dict | list | tuple):
            raise TypeError(f"Cannot convert <{items}> to dictionary")
        if not items:
            raise TypeError("Missing required positional argument: 'items'")

        if isinstance(items, dict):
            [self.__setitem__(key, value) for key, value in items.items()]
            return
        if not isinstance(items[0], list | tuple):
            self.__setitem__(*items)
            return

        for item in items:
            if isinstance(item, list | tuple) and len(item) == 2:
                self.__setitem__(*item)
            elif isinstance(item, dict):
                [self.__setitem__(key, value) for key, value in item.items()]
            else:
                raise TypeError(f"Cannot convert <{item}> to dictionary entry")

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            if default:
                return default
            else:
                raise
        self.__delitem__(key)
        return value

    def __delitem__(self, key: Hashable) -> None:
        hash_index, dict_index = self.get_index(key)
        self.dictionary[dict_index] = None
        self.hash_table[hash_index] = -2
        self.length -= 1

    def clear(self) -> None:
        self.__init__()

    def set_index(self, hash_code: int, key: Hashable) -> (int, int):
        hash_i = hash_code % self.get_capacity()
        while self.hash_table[hash_i] != -1:
            if self.hash_table[hash_i] == -2:
                hash_i = hash_i + 1 if hash_i < self.get_capacity() - 1 else 0
                continue
            dict_i = self.hash_table[hash_i]
            if self.dictionary[dict_i][:2] == (hash_code, key):
                return hash_i, dict_i
            hash_i = hash_i + 1 if hash_i < self.get_capacity() - 1 else 0
        return hash_i, self.hash_table[hash_i]

    def get_index(self, key: Hashable) -> (int, int):
        hash_i = hash(key) % self.get_capacity()
        while True:
            dict_i = self.hash_table[hash_i]
            if dict_i == -1:
                raise KeyError(f"No such key <{key}> in the dictionary")
            if dict_i >= 0 and self.dictionary[dict_i][:2] == (hash(key), key):
                return hash_i, dict_i
            hash_i = hash_i + 1 if hash_i < self.get_capacity() - 1 else 0

    def resize(self) -> None:
        self.hash_table = [-1] * (self.get_capacity() * 2)
        i = 0
        while i < len(self.dictionary):
            if self.dictionary[i]:
                hash_code, key, _ = self.dictionary[i]
                hash_index, _ = self.set_index(hash_code, key)
                self.hash_table[hash_index] = i
                i += 1
            else:
                self.dictionary.pop(i)

    def get_load_factor(self) -> float:
        return self.get_capacity() * 2 / 3

    def get_capacity(self) -> int:
        return len(self.hash_table)

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Any:
        return (item[1] for item in self.dictionary if item)

    def __str__(self) -> str:
        items = ""
        for d in self.dictionary:
            if not d:
                continue
            if items:
                items += ", "
            items += f"{d[1]}: {d[2]}"
        return "{" + items + "}"

    def __repr__(self) -> str:
        return self.__str__()
