from typing import Any, Iterable, Iterator, Tuple


class Dictionary:

    def __init__(self) -> None:
        self.keys: list[Any] = []
        self.values: list[Any] = []

    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            index = self.keys.index(key)
            self.values[index] = value
        except ValueError:
            self.keys.append(key)
            self.values.append(value)

    def __getitem__(self, key: Any) -> Any:
        try:
            index = self.keys.index(key)
            return self.values[index]
        except ValueError:
            raise KeyError

    def __delitem__(self, key: Any) -> None:
        index = self.keys.index(key)
        del self.keys[index]
        del self.values[index]

    def __iter__(self) -> Iterator[Any]:
        return iter(self.keys)

    def __len__(self) -> int:
        return len(self.keys)

    def clear(self) -> None:
        self.keys = []
        self.values = []

    def get(self, key: Any) -> Any:
        return self[key]

    def pop(self, key: Any) -> Any:
        index = self.keys.index(key)
        value = self.values[index]
        del self.keys[index]
        del self.values[index]
        return value

    def update(self, other: Iterable[Tuple[Any, Any]]) -> None:
        for key, value in other.items():
            self[key] = value
