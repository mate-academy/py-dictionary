from typing import Any, Optional


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.length: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        n = Node(key, value)
        i = hash(n.key) % self.capacity
        flag = False
        while not flag:
            if self.table[i] is None:
                if (self.length + 1) / self.capacity <= 2 / 3:
                    self.table[i] = n
                    self.length += 1
                    flag = True
                else:
                    self.capacity *= 2
                    temp = self.table.copy()
                    self.table = [None] * self.capacity
                    self.length = 0

                    for slot in temp:
                        if slot is not None:
                            self.__setitem__(slot.key, slot.value)

                    self.__setitem__(n.key, n.value)
                    flag = True
            else:
                if self.table[i].key == n.key:
                    self.table[i].value = n.value
                    flag = True
                else:
                    i = (i + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        i = hash(key) % self.capacity
        while True:
            if self.table[i] is None:
                raise KeyError(key)
            if self.table[i].key == key:
                return self.table[i].value

            i = (i + 1) % self.capacity

    def __len__(self) -> int:
        return self.length
