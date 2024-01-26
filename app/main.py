from typing import Any
from app.point import Point


class Node:
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 16, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: str, value: Any) -> None:
        index = self._get_index(key)
        node = Node(key, value)

        if self.table[index] is None:
            self.table[index] = [node]
        else:
            for existing_node in self.table[index]:
                if existing_node.key == key:
                    existing_node.value = value
                    break
            else:
                # Add new key
                self.table[index].append(node)

        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: str) -> Any:
        index = self._get_index(key)
        if self.table[index] is not None:
            for node in self.table[index]:
                if node.key == key:
                    return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        count = sum(len(chain) for chain in self.table if chain is not None)
        return count

    def _get_index(self, key: str) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for chain in self.table:
            if chain is not None:
                for node in chain:
                    index = hash(node.key) % self.capacity
                    if new_table[index] is None:
                        new_table[index] = [node]
                    else:
                        new_table[index].append(node)

        self.table = new_table


if __name__ == "__main__":
    my_dict = Dictionary()

    point1 = Point(1.0, 2.0)
    point2 = Point(3.0, 4.0)

    my_dict[point1] = "Value1"
    my_dict[point2] = "Value2"

    print(my_dict[point1])
    print(my_dict[point2])
    print(len(my_dict))
