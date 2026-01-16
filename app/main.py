from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_factor = 2 / 3
        self.capacity = 8

    def __setitem__(self, key: Any, value: Any) -> None:
        if not hasattr(key, "__hash__"):
            raise TypeError(f"Key '{key}' is not hashable.")

        hash_value = self._hash_function(key)
        node = (key, hash_value, value)

        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = [node]
        else:
            for i, (stored_key, _, _) \
                    in enumerate(self.hash_table[hash_value]):
                if stored_key == key:
                    self.hash_table[hash_value][i] = node
                    break
            else:
                self.hash_table[hash_value].append(node)

        if self.length > self.capacity * self.load_factor:
            self._resize()

        self.length = sum(len(chain) for chain in self.hash_table if chain)

    def __getitem__(self, key: Any) -> None:
        if not isinstance(key, (int, slice, str, float)) \
                and not hasattr(key, "__hash__"):
            raise TypeError("Key should be an integer, slice, or string.")

        hash_value = self._hash_function(key)
        chain = self.hash_table[hash_value]

        if chain:
            for stored_key, _, value in chain:
                if stored_key == key:
                    return value

        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def _hash_function(self, key: Any) -> int:
        return hash(key) % len(self.hash_table)

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for chain in self.hash_table:
            if chain:
                for stored_key, hash_val, value in chain:
                    hash_value = hash(stored_key) % new_capacity
                    new_node = (stored_key, hash_value, value)

                    if new_table[hash_value] is None:
                        new_table[hash_value] = [new_node]
                    else:
                        new_table[hash_value].append(new_node)

        self.capacity = new_capacity
        self.hash_table = new_table

    def __delitem__(self, key: Any) -> None:
        hash_value = self._hash_function(key)
        chain = self.hash_table[hash_value]

        if chain:
            new_chain = [(stored_key, hash_val, value)
                         for stored_key, hash_val, value
                         in chain if stored_key != key]

            if len(new_chain) < len(chain):
                self.hash_table[hash_value] = new_chain
                self.length -= 1
                return

        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def __len__(self) -> int:
        return self.length
