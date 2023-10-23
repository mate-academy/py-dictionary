from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor

        self.table = [None] * capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.__resize()

        index = self.__hash(key)
        if self.table[index] is None:
            self.table[index] = [(key, hash(key), value)]
        else:
            for i, (k, _, _) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, hash(key), value)
                    return
            self.table[index].append((key, hash(key), value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__hash(key)
        if self.table[index] is not None:
            for k, _, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Unknown key '{key}'!")

    def __len__(self) -> int:
        return self.size

    def __hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for bucket in self.table:
            if bucket is not None:
                for key, h, value in bucket:
                    index = h % new_capacity
                    if new_table[index] is None:
                        new_table[index] = [(key, h, value)]
                    else:
                        new_table[index].append((key, h, value))

        self.table = new_table
        self.capacity = new_capacity
