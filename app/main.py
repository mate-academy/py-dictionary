from typing import Any


class HashNode:
    def __init__(
            self, key: int | float | complex | str | tuple | object,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.loaded = int(self.capacity * (2 / 3))
        self.hash_table = [None] * self.capacity

    def get_hash_table_load_info(self) -> str:
        current_load = len(self.hash_table) - self.hash_table.count(None)
        expected_load = self.loaded + 1
        return (
            "is Load" if current_load == expected_load else "is not Load"
        )

    @staticmethod
    def check_key_type(key: Any) -> None:
        if isinstance(key, (set, dict, list)):
            raise TypeError(f"unhashable type: '{type(key)}'")

    def input_hash_data(self, node_pair: HashNode) -> None:
        index = node_pair.hash % self.capacity
        if self.hash_table[index] is None:
            self.hash_table[index] = node_pair
        elif self.hash_table[index].key == node_pair.key:
            self.hash_table[index].value = node_pair.value
        else:
            while self.hash_table[index] is not None:
                if self.hash_table[index].key == node_pair.key:
                    self.hash_table[index].value = node_pair.value
                    return
                index = (index + 1) % self.capacity
            self.hash_table[index] = node_pair

    def resize_hash_table(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.loaded = int(self.capacity * (2 / 3))
        for node_pair in old_hash_table:
            if node_pair is not None:
                self.input_hash_data(node_pair)

    def __setitem__(
            self, key: int | float | complex | str | tuple | object,
            value: Any) -> None:
        self.check_key_type(key)
        item = HashNode(key, value)
        if self.get_hash_table_load_info() == "is Load":
            self.resize_hash_table()
        self.input_hash_data(item)

    def __getitem__(
            self, item: int | float | complex | str | tuple | object
    ) -> Any | None:
        self.check_key_type(item)
        for node_pair in self.hash_table:
            if node_pair is not None and node_pair.key == item:
                return node_pair.value
        raise KeyError(item)

    def __len__(self) -> int:
        return len(self.hash_table) - self.hash_table.count(None)

    def pop(self, key: int | float | complex | str | tuple | object,
            def_value: Any = None) -> Any | None:
        self.check_key_type(key)
        for index, node_pair in enumerate(self.hash_table):
            if node_pair is not None and node_pair.key == key:
                value = node_pair.value
                self.hash_table[index] = None
                return value
        if def_value is None:
            raise KeyError(key)
        return def_value

    def clear(self) -> None:
        self.capacity = 8
        self.loaded = int(self.capacity * (2 / 3))
        self.hash_table = [None] * self.capacity

    def __delitem__(
            self, key: int | float | complex | str | tuple | object
    ) -> None:
        self.check_key_type(key)
        for index, node_pair in enumerate(self.hash_table):
            if node_pair is not None and node_pair.key == key:
                self.hash_table[index] = None
                return
        raise KeyError(key)

    def get(
            self, key: int | float | complex | str | tuple | object,
            def_value: Any = None) -> Any | None:
        self.check_key_type(key)
        for index, node_pair in enumerate(self.hash_table):
            if node_pair is not None and node_pair.key == key:
                return node_pair.value
        return def_value
