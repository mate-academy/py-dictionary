from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.load = 0
        self.items: list = [None] * 8

    def __len__(self) -> int:
        return self.load

    def __setitem__(self, key: Any, value: Any) -> None:
        lengths = len(self.items)
        new_hash = hash(key)
        index = new_hash % lengths

        if self.load > round(lengths * (2 / 3)):
            self.items += [None] * lengths
            self._rehash()

        for i in range(lengths):
            if self.items[i] is not None and self.items[i][0] == key:
                self.items[i][-1] = value
                return

        if self.items[index] is None:
            self.items[index] = [key, new_hash, value]
            self.load += 1
            return

        count = index
        for _ in range(len(self.items[index:]) - 1):
            count += 1
            if self.items[count] is None:
                self.items[count] = [key, new_hash, value]
                self.load += 1
                return

        for i in range(lengths):
            if self.items[i] is None:
                self.items[i] = [key, new_hash, value]
                self.load += 1
                break

    def __getitem__(self, key: Any) -> Any:
        for index in self.items:
            if index is not None and key == index[0]:
                return index[-1]
        raise KeyError

    def _rehash(self) -> None:
        lengths = len(self.items)
        create_new = [None] * lengths
        for item in self.items:
            index = None
            if item is not None:
                index = item[1] % len(create_new)
            if index is not None and create_new[index] is None:
                create_new[index] = item
                return
        self.items = create_new
