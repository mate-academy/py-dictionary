from collections.abc import Hashable, Iterable


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value

    def __repr__(self) -> str:
        return (
            f"Node(key={self.key}, "
            f"hash_value={self.hash_value}, "
            f"value={self.value})"
        )


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 0.7
        self.current_load: int = 0
        self.threshold: float = self.capacity * self.load_factor
        self.hash_table: list[Node | None | Iterable] = [None] * self.capacity

    def __repr__(self) -> str:
        return str(
            {
                element.key: element.value
                for element in self.hash_table
                if isinstance(element, Node)
            }
        )

    def renew_capacity(self) -> None:
        old_hash_table = [
            node for node in self.hash_table if isinstance(node, Node)
        ]
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.threshold = self.capacity * self.load_factor
        for node in old_hash_table:
            index = node.hash_value % self.capacity
            while self.hash_table[index] is not None:
                index = (index + 1) % self.capacity
            self.hash_table[index] = node

    def __setitem__(self, key: Hashable, values: any) -> None:
        if isinstance(key, list | set | dict):
            raise TypeError(f"unhashable type: {type(key)}")

        hash_value = hash(key)
        index = hash_value % self.capacity
        deleted_cell = None

        while (cell := self.hash_table[index]) not in {None, "DELETED"}:
            if cell == "DELETED" and deleted_cell is None:
                deleted_cell = index
            if cell.key == key:
                cell.value = values
                return
            index = (index + 1) % self.capacity

        if deleted_cell is not None:
            index = deleted_cell

        self.hash_table[index] = Node(key, hash_value, values)
        self.current_load += 1

        if self.current_load >= self.threshold:
            self.renew_capacity()

    def __getitem__(self, key: Hashable) -> any:
        index = hash(key) % self.capacity
        while (cell := self.hash_table[index]) not in {None, "DELETED"}:
            if cell.key == key:
                return cell.value
            index = (index + 1) % self.capacity
        raise KeyError(f"KeyError: {key}")

    def __len__(self) -> int:
        return self.current_load

    # _________________addition methods_____________________
    def __iter__(self) -> any:
        for cell in self.hash_table:
            if isinstance(cell, Node):
                yield cell.key

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = 0.7
        self.current_load = 0
        self.threshold = self.capacity * self.load_factor
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while (cell := self.hash_table[index]) not in {None, "DELETED"}:
            if cell.key == key:
                self.hash_table[index] = "DELETED"
                self.current_load -= 1
                return

        raise KeyError(f"KeyError: {key}")

    def get(self, key: Hashable, default: None = None) -> any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while (cell := self.hash_table[index]) not in {None, "DELETED"}:
            if cell.key == key:
                return cell.value

            index = (index + 1) % self.capacity
        return default

    def pop(self, key: Hashable, default: any = None) -> any:
        index = hash(key) % self.capacity
        while (cell := self.hash_table[index]) not in {None, "DELETED"}:
            if cell.key == key:
                value = cell.value
                self.hash_table[index] = "DELETED"
                self.current_load -= 1
                return value

        if default is not None:
            return default

        raise KeyError(f"KeyError: {key}")

    def update(self, other: any) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
            return

        if not isinstance(other, Dictionary):
            raise TypeError("cannot convert dictionary update wrong type")
        for node in other.hash_table:
            if isinstance(node, Node):
                index = node.hash_value % self.capacity
                while (cell := self.hash_table[index]) not in {
                    None,
                    "DELETED",
                }:  # noqa: E501
                    if cell.key == node.key:
                        cell.value = node.value
                        break
                    index = (index + 1) % self.capacity

                self.hash_table[index] = node
                self.current_load += 1

                if self.current_load >= self.threshold:
                    self.renew_capacity()

    def items(self) -> list:
        return [
            (cell.key, cell.value)
            for cell in self.hash_table
            if isinstance(cell, Node)
        ]

    def values(self) -> list:
        return [
            cell.value for cell in self.hash_table if isinstance(cell, Node)
        ]

    def keys(self) -> list:
        return [cell.key for cell in self.hash_table if isinstance(cell, Node)]
