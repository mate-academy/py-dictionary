from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.length

    def hash_func(self, key: Any) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0
        for bucket in old_table:
            for key, _, value in bucket:
                self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > self.capacity * 0.7:
            self.resize()
        index = self.hash_func(key)
        has_collision = False
        collision_index = 0
        node = self.hash_table[index]
        item_to_add = (key, hash(key), value)

        for node_index, item in enumerate(node):
            key_item, _, _ = item
            if key_item == key:
                has_collision = True
                collision_index = node_index
                break

        if has_collision:
            node[collision_index] = item_to_add
        else:
            node.append(item_to_add)
            self.length += 1

    def __getitem__(self, item_key: Any) -> Any:
        index = self.hash_func(item_key)
        for item in self.hash_table[index]:
            key, _, value = item
            if key == item_key:
                return value
        raise KeyError(f'Key not found: {item_key}')

    def __delitem__(self, key: Any) -> None:
        index = self.hash_func(key)
        pop_value = self.__getitem__(key)
        item_to_delete = (key, hash(key), pop_value)

        self.hash_table[index].remove(item_to_delete)
        self.length -= 1

    def clear(self) -> None:
        self.hash_table: list = [[] for _ in range(self.capacity)]
        self.length = 0

    def get(
            self,
            key: Any,
            default_return: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_return

    def pop(
            self,
            key: Any,
            default_return: Any = 0) -> Any:
        try:
            return_item = self.__getitem__(key)
            self.__delitem__(key)
            return return_item
        except KeyError:
            return default_return

    def update(self, other_dict: Any) -> None:
        for key in other_dict:
            self.__setitem__(key, other_dict[key])

    def __iter__(self) -> Any:
        for index in range(self.capacity):
            for item in self.hash_table[index]:
                key, _, _ = item
                yield key
