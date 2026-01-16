from typing import Any, Iterator, Union, Optional


class Dictionary:
    def __init__(self, capacity: int = 8, size: int = 0) -> None:
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.size = size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= round(self.capacity * (2 / 3)):
            self._resize()

        hash_value = hash(key)
        index = hash_value % self.capacity

        free_index = index
        while self.table[free_index] is not None:
            if self.table[free_index][0] == key:
                self.table[free_index] = (key, value)
                return
            free_index = (free_index + 1) % self.capacity

        self.table[free_index] = (key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        start_index = index

        while self.table[index]:
            if self.table[index] != "DELETED" and key == self.table[index][0]:
                return self.table[index][1]
            index = (index + 1) % self.capacity

            if index == start_index:
                break

        raise KeyError("Key not found")

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        start_index = index

        while self.table[index]:
            if self.table[index] != "DELETED" and key == self.table[index][0]:
                self.table[index] = "DELETED"
                self.size -= 1
                return
            index = (index + 1) % self.capacity

            if index == start_index:
                break

        raise KeyError("Key not found")

    def __iter__(self) -> Iterator[Any]:
        keys = []
        for item in self.table:
            if item:
                key, value = item
                keys.append(key)
        return iter(keys)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item:
                key, value = item
                self.__setitem__(key, value)

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        item = self.get(key)
        if item:
            self.__delitem__(key)
            return item
        return default

    def update(
            self, other_dict: Union[dict[Any, Any], list[tuple[Any, Any]]]
    ) -> None:
        if not isinstance(other_dict, dict):
            for item in other_dict:
                key, value = item
                self[key] = value
        else:
            for key, value in other_dict.items():
                self[key] = value
