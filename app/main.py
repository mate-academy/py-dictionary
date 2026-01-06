from typing import Any, Hashable


class Tombstone:
    def __bool__(self) -> bool:
        return False


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list[None | Node | Tombstone] = [None] * 8
        self.reserved_count = 0
        self.real_size = 8

    def find_index(self, key: Hashable) -> int | None:
        idx = hash(key) % self.real_size
        for _ in range(self.real_size):
            node = self.hash_table[idx]
            if node and node.key == key:
                return idx
            else:
                idx = (idx + 1) % self.real_size
        return None

    def save(self, saving_node: Node) -> None:
        idx = saving_node.hash % self.real_size
        for _ in range(self.real_size):
            node = self.hash_table[idx]

            if node and node.key == saving_node.key:
                self.hash_table[idx].value = saving_node.value
                return

            elif not node:
                self.hash_table[idx] = saving_node
                self.reserved_count += 1
                return

            idx = (idx + 1) % self.real_size

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.save(Node(key, value))

        if self.reserved_count > self.real_size * 0.66:
            old_nodes = [node for node in self.hash_table if node]
            self.reserved_count = 0
            self.real_size *= 2
            self.hash_table = [None] * self.real_size
            for node in old_nodes:
                self.save(node)

    def __getitem__(self, key: Hashable) -> Any:
        searched_key = self.find_index(key)
        if searched_key is not None:
            return self.hash_table[searched_key].value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.reserved_count

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.reserved_count = 0
        self.real_size = 8

    def __delitem__(self, key: Hashable) -> None:
        searched_key = self.find_index(key)
        if searched_key is not None:
            self.hash_table[searched_key] = Tombstone()
            self.reserved_count -= 1
            return
        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        searched_key = self.find_index(key)
        if searched_key is not None:
            output = self.hash_table[searched_key].value
            self.hash_table[searched_key] = Tombstone()
            self.reserved_count -= 1
            return output

        elif default:
            return default

        raise KeyError(key)

    def update(self, array: dict) -> None:
        for key, value in array.items():
            self.__setitem__(key, value)

    def __iter__(self) -> Any:
        for node in self.hash_table:
            if isinstance(node, Node):
                yield node.key
