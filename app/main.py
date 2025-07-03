from typing import Hashable, Any


class Dictionary:
    def __init__(self, size: int = 8) -> None:
        self.data_storage = [[] for _ in range(size)]
        self.size = size

    def resize_check(self) -> int:
        return len(self) / self.size >= 2 / 3

    def __len__(self) -> int:
        return sum(len(element) for element
                   in self.data_storage)

    def __setitem__(self, key: Hashable,
                    value: Any) -> None:
        if self.resize_check():
            self.resize()
        try:
            index = hash(key) % self.size
        except TypeError:
            raise TypeError(f"{key} is not a hashable object")

        data_container = self.data_storage[index]
        for i , (k, v) in enumerate(data_container):
            if k == key:
                data_container[i] = (key, value)
                return
        data_container.append((key, value))

    def resize(self) -> None:
        old_storage = self.data_storage
        self.size *= 2
        self.data_storage = [[] for _ in range(self.size)]

        for element in old_storage:
            for key, value in element:
                index = hash(key) % self.size
                self.data_storage[index].append((key, value))

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.size
        data_cell = self.data_storage[index]

        for k, v in data_cell:
            if k == key:
                return v

        raise KeyError(f"Key {key} does not exist.")
