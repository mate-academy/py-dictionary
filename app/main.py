from typing import Hashable, Any, Iterable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any,
            hash_val: int = None
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key) if hash_val is None else hash_val


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: int = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = self.create_table()

    def create_table(self) -> []:
        return [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_val = hash(key)
        store_index = hash_val % self.capacity
        while self.table[store_index]:
            if self.table[store_index][0].key == key:
                self.table[store_index][0].value = value
                break
            else:
                store_index += 1
                if store_index >= len(self.table) - 1:
                    store_index = 0
        else:
            store = self.table[store_index]
            store.append(Node(key, value, hash_val))
            self.size += 1
            if self.size >= self.capacity * self.load_factor:
                self.resize()

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = self.create_table()
        self.size = 0
        for store in old_table:
            if store:
                self.__setitem__(store[0].key, store[0].value)

    def __getitem__(self, key: Hashable) -> Any:
        hash_val = hash(key)
        store_index = hash_val % self.capacity
        while self.table[store_index]:
            if self.table[store_index][0].key == key:
                return self.table[store_index][0].value
            store_index += 1
            if store_index >= len(self.table) - 1:
                store_index = 0
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        hash_val = hash(key)
        store = self.table[hash_val % self.capacity]
        for i, node in enumerate(store):
            if node.key == key:
                del store[i]
                self.size -= 1
                return
        raise KeyError(key)

    def clear(self) -> None:
        self.size = 0
        self.table = self.create_table()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:

        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default:
                return default
            raise

    def update(self, other: Iterable | dict) -> None:

        if isinstance(other, Iterable | Dictionary | dict):
            if isinstance(other, Dictionary | dict):

                for key in other:
                    self.__setitem__(key, other[key])

            else:
                for key, value in other:
                    self.__setitem__(key, value)

    def __iter__(self) -> None:
        for store in self.table:
            for node in store:
                yield node.key
