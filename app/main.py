from typing import Any


class Node:
    """Вузол для зберігання пари ключ-значення у хеш-таблиці."""
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        """Збільшує розмір хеш-таблиці для підтримки ефективності."""
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Додає або оновлює пару ключ-значення."""
        if self.length >= self.capacity * 2 // 3:
            self._resize()

        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if (self.hash_table[index].hash == hash_value
                    and self.hash_table[index].key == key):
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = Node(key, hash_value, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        """Отримує значення за заданим ключем."""
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if (self.hash_table[index].hash == hash_value
                    and self.hash_table[index].key == key):
                return self.hash_table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in the dictionary.")
