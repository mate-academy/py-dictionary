from typing import Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = Dictionary.INITIAL_CAPACITY
        self.hash_table = [0 for _ in range(self.capacity)]
        self.size = 0

    def resize(self) -> None:
        if self.size <= int(self.capacity * Dictionary.LOAD_FACTOR):
            return
        self.capacity *= 2
        self.size = 0
        old_hash_table = self.hash_table
        self.hash_table = [0 for _ in range(self.capacity)]
        for element in old_hash_table:
            if isinstance(element, tuple):
                self.__setitem__(element[0], element[2])

    def key_exists(self, key: Any) -> [tuple, None]:
        for element in self.hash_table:
            if isinstance(element, tuple) and element[0] == key:
                return self.hash_table.index(element)
        return None

    def __setitem__(self, key: Any, value: Any) -> None:
        self.resize()
        key_check = self.key_exists(key)
        if key_check is not None:
            hash_table_index = key_check
        else:
            temporary = 0
            while True:  # getting a hash table index with checks for collision
                hash_table_index = (hash(key) + temporary) % self.capacity
                if not isinstance(self.hash_table[hash_table_index], tuple):
                    self.size += 1
                    break
                temporary += 1

        self.hash_table[hash_table_index] = (key, hash(key), value)

    def __getitem__(self, key: Any) -> Any:
        key_check = self.key_exists(key)
        if key_check is not None:
            return self.hash_table[key_check][2]
        else:
            raise KeyError

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        dict_elements = ", ".join(f"{element[0]}: {element[2]}"
                                  for element in self.hash_table
                                  if isinstance(element, tuple))
        return f"{{{dict_elements}}}"

    def __sizeof__(self) -> int:
        return len(self.hash_table)
