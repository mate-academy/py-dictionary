from collections.abc import Hashable, Iterable
from typing import Any


class Dictionary:

    def __init__(self, data: list = []) -> None:
        self.keys = []
        self.values = []
        if data and isinstance(data, Iterable):
            for el in data:
                self.__setitem__(el[0], el[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        elif key in self.keys:
            self.values[self.keys.index(key)] = value
        else:
            self.keys.append(key)
            self.values.append(value)

    def __getitem__(self, key: Hashable) -> Any:
        if key in self.keys:
            return self.values[self.keys.index(key)]
        else:
            raise KeyError("No such key")

    def __len__(self) -> int:
        return len(self.keys)

    def __repr__(self) -> str:
        res = "{"
        for key, value in zip(self.keys, self.values):
            res += f"({key} : {value})"
        return res + "}"

    def __delitem__(self, key: Hashable) -> None:
        if key in self.keys:
            indx = self.keys.index(key)
            del self.keys[indx]
            del self.values[indx]
        else:
            raise KeyError("No such key")


if __name__ == "__main__":
    pass
