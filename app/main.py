from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.__initial_capacity: int = 8
        self.__load_factor: float = 2 / 3
        self.__resize_strategy: int = 2
        self.__capacity: int = self.__initial_capacity
        self.__threshold: int = self.get_threshold()
        self.__hash_table: list[tuple[Any, int, Any]]\
            = [None] * self.__capacity
        self.__len = 0

    def __str__(self) -> str:
        _str = "{"
        for node_value in (node_value
                           for node_value in self.__hash_table
                           if node_value is not None):
            if _str != "{":
                _str += ", "
            _str += f"{node_value[0]}: {node_value[2]}"

        _str += "}"
        return _str

    def __repr__(self) -> str:
        return self.__str__()

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.__len >= self.__threshold:
            self.resize_hash_table()

        node_value = self.get_node_value(key, value)
        self.__set_node_value(self.__hash_table, node_value)

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(hash(key))
        for _ in range(0, self.__capacity):
            if self.__hash_table[index] is not None:
                if key == self.__hash_table[index][0]:
                    return self.__hash_table[index][2]

            index = (index + 1) % self.__capacity

        raise KeyError("Element not found by key")

    def __len__(self) -> int:
        return self.__len

    @staticmethod
    def get_node_value(key: Any, value: Any) -> tuple[Any, int, Any]:
        return key, hash(key), value

    def get_index(self, hash_key: int) -> int:
        return hash_key % self.__capacity

    def get_threshold(self) -> int:
        return int(self.__capacity * self.__load_factor)

    def __set_node_value(self, hash_table: list[tuple[Any, int, Any]],
                         node_value: tuple[Any, int, Any]) -> None:
        index = self.get_index(node_value[1])

        for _ in range(0, self.__capacity):
            if hash_table[index] is None:
                hash_table[index] = node_value
                self.__len += 1
                return
            elif node_value[0] == hash_table[index][0]:
                hash_table[index] = node_value
                return

            index = (index + 1) % self.__capacity

    def resize_hash_table(self) -> None:
        self.__capacity *= self.__resize_strategy
        self.__threshold = self.get_threshold()
        new_hash_table: list[tuple[Any, int, Any]]\
            = [None] * self.__capacity

        self.__len = 0
        for node_value in (node_value
                           for node_value in self.__hash_table
                           if node_value is not None):
            self.__set_node_value(new_hash_table, node_value)

        self.__hash_table = new_hash_table

    def clear(self) -> None:
        self.__initial_capacity = self.__capacity
        self.__hash_table: list[tuple[Any, int, Any]] \
            = [None] * self.__capacity
        self.__len = 0
        self.__threshold: int = self.get_threshold()

    def __delitem__(self, key: Any) -> None:
        index = self.get_index(hash(key))
        for _ in range(0, self.__capacity):
            if self.__hash_table[index] is not None:
                if key == self.__hash_table[index][0]:
                    self.__hash_table[index] = None
                    self.__len -= 1
                    return

            index = (index + 1) % self.__capacity

        raise KeyError("Element not found by key")

    def get(self, key: Any, default_value: Any = None) -> Any:
        index = self.get_index(hash(key))

        for _ in range(0, self.__capacity):
            if self.__hash_table[index] is None:
                return default_value
            elif key == self.__hash_table[index][0]:
                return self.__hash_table[index][2]

            index = (index + 1) % self.__capacity

        return default_value

    def pop(self, key: Any, default_value: Any = None) -> Any:
        value = self.get(key, default_value)
        if value is None:
            raise KeyError("Element not found by key")
        self.__delitem__(key)
        return value

    def __iter__(self) -> Any:
        list_keys = [node_value[0]
                     for node_value in self.__hash_table
                     if node_value is not None]
        return iter(list_keys)
