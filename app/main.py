from typing import Any


class ClassKeyValue:
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.key_value_table: list = [None] * 8
        # self.index = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: str, value: Any) -> None:
        if self.length / len(self.key_value_table) >= 0.75:
            self.double_size()
        index = self.get_index(key)

        for _ in range(len(self.key_value_table)):
            key_value = self.key_value_table[index]
            if key_value is None:
                self.key_value_table[index] = ClassKeyValue(key, value)
                self.length += 1
                return
            if self.key_value_table[index].key == key:
                self.key_value_table[index].value = value
                return

            index = (index + 1) % len(self.key_value_table)

    def __getitem__(self, key: str) -> Any:
        index = self.get_index(key)
        for _ in range(len(self.key_value_table)):
            key_value = self.key_value_table[index]
            if key_value is not None and key_value.key == key:
                return key_value.value
            index = (index + 1) % len(self.key_value_table)

        raise KeyError(f"Key '{key}' not found.")

    def double_size(self) -> None:
        old_table = self.key_value_table
        self.key_value_table = [None] * (len(old_table) * 2)
        self.length = 0

        for key_value in old_table:
            if key_value is not None:
                self.__setitem__(key_value.key, key_value.value)

    def get_index(self, key: str) -> int:
        return hash(key) % len(self.key_value_table)
