from typing import Any, Hashable, Iterable, Mapping


class Dictionary:
    def __init__(self) -> None:
        self.len_of_dict = 8
        self.resize_value = 0.7
        self.quantity_key = 0
        self.container = [[] for _ in range(self.len_of_dict)]

    def __delitem__(self, key: Hashable) -> None:
        index = self.hash_formula(key)

        if self.container[index]:
            for i, (k, v) in enumerate(self.container[index]):
                if k == key:
                    del self.container[index][i]
                    self.quantity_key -= 1
                    return

        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.quantity_key >= self.len_of_dict * self.resize_value:
            self.resize()

        index = self.hash_formula(key)

        for i, (k, v) in enumerate(self.container[index]):
            if k == key:
                self.container[index][i] = (key, value)
                return

        self.container[index].append((key, value))
        self.quantity_key += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash_formula(key)

        for k, v in self.container[index]:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.quantity_key

    def hash_formula(self, key: Hashable) -> int:
        return hash(key) % self.len_of_dict

    def resize(self) -> None:
        self.len_of_dict *= 2
        new_container = [[] for _ in range(self.len_of_dict)]

        for bucket in self.container:
            for key, value in bucket:
                new_index = self.hash_formula(key)
                new_container[new_index].append((key, value))

        self.container = new_container

    def clear(self) -> None:
        self.len_of_dict = 8
        self.resize_value = 0.7
        self.quantity_key = 0
        self.container = [[] for _ in range(self.len_of_dict)]

    def pop(self, key: Hashable) -> Any:
        index = self.hash_formula(key)
        if self.container[index]:
            for i, (k, v) in enumerate(self.container[index]):
                if k == key:
                    del self.container[index][i]
                    self.quantity_key -= 1
                    return v
        raise KeyError(f"Key {key} not found")

    def update(self, other: Iterable[tuple[Hashable, Any]]) -> None:
        if isinstance(other, Mapping):
            other = other.items()

        for key, value in other:
            self.__setitem__(key, value)
