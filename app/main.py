from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.table = [None] * 8
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % len(self.table)

        if self.table[index] is None:
            self.table[index] = [(key, value)]
            self.size += 1
        else:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return

            self.table[index].append((key, value))
            self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % len(self.table)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
