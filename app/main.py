from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._items = []

    def __setitem__(self, key: int, value: Any) -> None:
        for ind, (k, v) in enumerate(self._items):
            if k == key:
                self._items[ind] = (key, value)
                return
        self._items.append((key, value))

    def __getitem__(self, key: int) -> Any:
        for ind, (k, v) in enumerate(self._items):
            if k == key:
                return v
        raise KeyError

    def __len__(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items = []

    def __delitem__(self, key: int) -> None:
        for ind, (k, v) in enumerate(self._items):
            if k == key:
                del self._items[ind]
                return
        raise KeyError

    def get(self, key: int, default: Any = None) -> Any | None:
        for ind, (k, v) in enumerate(self._items):
            if k == key:
                return v
        return default

    def pop(self, ind: int = None) -> None:
        if ind:
            self._items.remove(self._items[ind])
        else:
            self._items.remove(self._items[-1])

    def update(self, update_values: list[tuple]) -> None:
        for k, v in update_values:
            for ind, (key, value) in enumerate(self._items):
                if key == k:
                    self._items[ind] = (k, v)
                    break
            else:
                self._items.append((k, v))

    def __iter__(self) -> None:
        for k, v in self._items:
            yield k
