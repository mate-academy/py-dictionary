from typing import Any, Union


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.table = [None] * capacity
        self.length = 0
        self.capacity = capacity
        self.initial_capacity = capacity  # for clear method

    def __setitem__(self, key: Any, value: Any) -> None:

        hash_value = hash(key)
        node = {"key": key, "value": value, "hash": hash_value}

        self.check_need_resize()

        index = self.count_position(hash_value)

        if self.table[index] is not None:
            found = False
            for el in self.table[index]:
                if el["key"] == key and el["hash"] == hash_value:
                    el["value"] = value
                    found = True
                    break
            if not found:
                self.length += 1
                self.table[index].append(node)

        else:
            self.length += 1
            self.table[index] = list()
            self.table[index].append(node)

    def __getitem__(self, key: Any) -> Any:
        search_hash = hash(key)
        index = self.count_position(search_hash)
        if self.table[index] is not None:
            for el in self.table[index]:
                if el["hash"] == search_hash and el["key"] == key:
                    return el["value"]
        raise KeyError(f"Key {key} not found!")

    def check_need_resize(self) -> None:
        load_factor = 2 / 3

        if (self.length + 1) / self.capacity >= load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for el in self.table:

            if el is not None:
                for chain_element in el:
                    index = self.count_position(chain_element["hash"],
                                                new_capacity)
                    if new_table[index] is not None:
                        new_table[index].append(chain_element)

                    else:
                        new_table[index] = list()
                        new_table[index].append(chain_element)

        self.table = new_table
        self.capacity = new_capacity

    def __len__(self) -> int:
        return self.length

    def count_position(self, hash_value: int,
                       capacity: Union[int, None] = None) -> int:
        if capacity is None:
            capacity = self.capacity
        return hash_value % capacity

    def clear(self) -> None:
        new_table = [None] * self.initial_capacity
        self.table = new_table
