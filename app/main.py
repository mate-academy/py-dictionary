from typing import Any


class Dictionary:

    def __init__(self, capacity=8) -> None:
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> Any:
        index = hash(key) % self.capacity
        buck = self.table[index]

        for i, (k, v) in enumerate(buck):
            if k == key:
                buck[i] = (key, value)
                return

        buck.append((key, value))
        self.size += 1

    def __getitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity
        back = self.table[index]

        for k, v in back:
            if k == item:
                return v

        raise KeyError(item)

    def __len__(self) -> int:
        return self.size
