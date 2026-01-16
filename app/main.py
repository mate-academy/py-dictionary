from typing import Any


# Item in custom dict contains key, hash and value.
# And can compare each other with its key and hash
class DictItem:
    def __init__(self, key: Any, value: Any = None) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DictItem):
            return self.key == other.key and self.hash == other.hash
        else:
            return False


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * (2 / 3))
        self.cells = [None] * self.capacity

    def __len__(self) -> int:
        length = 0
        for cell in self.cells:
            if cell is not None:
                length += 1

        return length

    def __setitem__(self, key: Any, value: Any) -> None:
        newitem = DictItem(key, value)
        index = newitem.hash % self.capacity

        # Index linear probing
        while True:
            if self.cells[index] is None:
                self.cells[index] = newitem
                break
            else:
                if self.cells[index] == newitem:
                    self.cells[index] = newitem
                    break
                else:
                    index = (index + 1) % self.capacity

        # Increasing size of dictionary
        if len(self) >= self.threshold:
            self.capacity *= 2
            self.threshold = int(self.capacity * (2 / 3))

            # Resigning items in cells
            self.cells = self._reassign()

    def _reassign(self) -> list[DictItem]:
        new_items_list = [None] * self.capacity

        for item in self.cells:
            if item is not None:
                index = item.hash % self.capacity
                while True:
                    if new_items_list[index] is None:
                        new_items_list[index] = item
                        break
                    else:
                        if new_items_list[index] == item:
                            new_items_list[index] = item
                            break
                        else:
                            index = (index + 1) % self.capacity

        return new_items_list

    def __getitem__(self, key: Any) -> Any:
        item_to_find = DictItem(key)
        index = item_to_find.hash % self.capacity

        while True:
            if self.cells[index] is None:
                raise KeyError(f"There is no item with key {item_to_find.key}")
            elif self.cells[index] == item_to_find:
                return self.cells[index].value
            else:
                index = (index + 1) % self.capacity

    def clear(self) -> None:
        self.cells = [None] * self.capacity

    def get(self, key: Any, value: Any = None) -> Any:
        try:
            result = self.__getitem__(key)
            return result
        except KeyError:
            return value

    def __iter__(self) -> DictItem:
        self.index = 0
        return self

    def __next__(self) -> DictItem:
        while self.index < self.capacity:
            current = self.cells[self.index]
            self.index += 1
            if current is not None:
                return current.key
        raise StopIteration

    def __delitem__(self, key: Any) -> None:
        item_to_delete = DictItem(key)
        index = item_to_delete.hash % self.capacity

        while True:
            if self.cells[index] is None:
                raise KeyError(f"There is no item with "
                               f"key {item_to_delete.key}")
            elif self.cells[index] == item_to_delete:
                self.cells[index] = None
                break
            else:
                index = (index + 1) % self.capacity

        # Resigning items in cells
        self.cells = self._reassign()

    def pop(self, key: Any, return_value: Any = None) -> Any:
        item_to_find = DictItem(key)
        index = item_to_find.hash % self.capacity

        while True:
            if self.cells[index] is None:
                if not return_value:
                    raise KeyError(f"There is no item with "
                                   f"key {item_to_find.key}")
                else:
                    return return_value
            elif self.cells[index] == item_to_find:
                item_to_return = self.cells[index]
                self.cells[index] = None
                break
            else:
                index = (index + 1) % self.capacity

        # Resigning items in cells
        self.cells = self._reassign()

        return item_to_return.value

    def update(self, key: Any, value: Any) -> None:
        item_to_update = DictItem(key, value)
        index = item_to_update.hash % self.capacity

        while True:
            if self.cells[index] is None:
                raise KeyError(f"There is no item with "
                               f"key {item_to_update.key}")
            elif self.cells[index] == item_to_update:
                self.cells[index].value = item_to_update.value
                break
            else:
                index = (index + 1) % self.capacity
