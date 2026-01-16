
from typing import Any


class Node:
    def __init__(self, key: object, hashed_key: int, value: Any) -> None:
        self.key = key
        self.hashed_key = hashed_key
        self.value = value

    def __repr__(self) -> str:
        return f"key: {self.key}, hash: {self.hashed_key}, value: {self.value}"


class Dictionary:
    def __init__(self) -> None:
        self.__load_factor = 2 / 3
        self.__capacity = 8
        self.__size = 0
        self.__table = [[] for _ in range(self.__capacity)]

    def validate_exist_key(self, key: object) -> (int, int, int | None):
        try:
            hashed_key = hash(key)
            table_index = hashed_key % self.__capacity
            for i, node in enumerate(self.__table[table_index]):
                if key == node.key:
                    return table_index, hashed_key, i
            return table_index, hashed_key, None
        except TypeError:
            raise

    def __setitem__(self, key: object, value: Any) -> Any:
        table_index, hashed_key, exist_key = self.validate_exist_key(key)
        if exist_key is not None:
            self.__table[table_index][exist_key].value = value
        else:
            self.__table[table_index].append(
                Node(key=key, hashed_key=hashed_key, value=value)
            )
            self.__size += 1
            self.resize_table()

    def __getitem__(self, key: object) -> Any:
        table_index, hashed_key, exist_key = self.validate_exist_key(key)
        if exist_key is not None:
            return self.__table[table_index][exist_key].value
        raise KeyError(f"{key}")

    def __len__(self) -> int:
        return self.__size

    def resize_table(self) -> None:
        if self.__size >= self.__load_factor * self.__capacity:
            self.__capacity *= 2
            new_table = [[] for _ in range(self.__capacity)]
            for cell in self.__table:
                for node in cell:
                    index = node.hashed_key % self.__capacity
                    new_table[index].append(node)
            self.__table = new_table

    def __repr__(self) -> str:
        return f"{self.__table}"

    def clear(self) -> None:
        self.__capacity = 8
        self.__size = 0
        self.__table = [[] for _ in range(self.__capacity)]

    def get(self, key: object) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: object) -> Any:
        table_index, hashed_key, exist_key = self.validate_exist_key(key)
        if exist_key is not None:
            node = self.__table[table_index][exist_key]
            value = node.value
            self.__table[table_index].pop(exist_key)
            self.__size -= 1
            return value
        raise KeyError(f"{key}")

    def __delitem__(self, key: object) -> None:
        table_index, hashed_key, exist_key = self.validate_exist_key(key)
        if exist_key is not None:
            del self.__table[table_index][exist_key]
            self.__size -= 1

    def update(self, key: object, value: Any) -> None:
        self.__setitem__(key, value)
        return None

    def __iter__(self) -> Any:
        for cell in self.__table:
            for node in cell:
                yield node.value
