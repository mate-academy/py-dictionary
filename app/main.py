from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: int | float | bool | str | tuple | Hashable,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(
            self,
            capacity: int = 8,
            load_factor: float = 2 / 3,
            size_of_dict: int = 0
    ) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size_of_dict = size_of_dict
        self.resize = int(self.capacity * self.load_factor)
        self.hash_table = [None for _ in range(self.capacity)]

    def set_element(self, item: Node) -> None:
        index = item.hash % self.capacity

        while self.hash_table[index]:
            if (
                    self.hash_table[index].key == item.key
                    and hash(self.hash_table[index].key) == item.hash
            ):
                self.hash_table[index].value = item.value
                return

            index += 1
            index %= self.capacity

        self.hash_table[index] = item
        self.size_of_dict += 1

    def resize_hash_table(self, item: Node) -> None:
        self.capacity *= 2
        self.resize = int(self.capacity * self.load_factor)
        elements_to_shift = [
            element for element in self.hash_table if element is not None
        ]
        self.hash_table = [None for _ in range(self.capacity)]
        self.size_of_dict = 0
        for element in elements_to_shift:
            self.set_element(element)
        self.set_element(item)

    def __setitem__(
            self,
            key: int | float | bool | str | tuple | Hashable,
            value: Any
    ) -> None:
        item = Node(key=key, value=value)

        if self.size_of_dict >= self.resize:
            self.resize_hash_table(item)
        else:
            self.set_element(item)

    def find_index_of_item(
            self,
            index: int,
            item: int | float | bool | str | tuple | Hashable
    ) -> int | None:
        for _ in range(self.capacity):
            if not self.hash_table[index]:
                index += 1
                index %= self.capacity
            elif self.hash_table[index].key == item:
                return index
            else:
                index += 1
                index %= self.capacity

    def __getitem__(
            self,
            item: int | float | bool | str | tuple | Hashable
    ) -> Any:
        item_hash = hash(item)
        index = item_hash % self.capacity

        result = self.find_index_of_item(index=index, item=item)
        if result is not None:
            return self.hash_table[result].value
        raise KeyError(f"No such key:'{item}' in dictionary")

    def __len__(self) -> int:
        return self.size_of_dict

    def clear(self) -> None:
        self.capacity = 8
        self.size_of_dict = 0
        self.hash_table = [None for _ in range(self.capacity)]

    def __delitem__(
            self,
            key: int | float | bool | str | tuple | Hashable
    ) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        result = self.find_index_of_item(index=index, item=key)
        if result is not None:
            self.hash_table[result] = None
            self.size_of_dict -= 1
        else:
            raise KeyError(
                f"Can't be deleted! No such key:'{key}' in dictionary"
            )

    def get(
            self,
            key: int | float | bool | str | tuple | Hashable,
            value: Any = None
    ) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        result = self.find_index_of_item(index=index, item=key)
        if result is not None:
            return self.hash_table[result].value
        return value

    def pop(
            self,
            keyname: int | float | bool | str | tuple | Hashable,
            defaultvalue: Any
    ) -> Any:
        key_hash = hash(keyname)
        index = key_hash % self.capacity
        result = self.find_index_of_item(index=index, item=keyname)
        if result is not None:
            return_value = self.hash_table[result].value
            self.hash_table[result] = None
            self.size_of_dict -= 1
            return return_value
        if defaultvalue:
            return defaultvalue
        raise KeyError
