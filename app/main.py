from typing import Hashable, Any, Iterator, Iterable


class Node:
    def __init__(
            self,
            key: Hashable,
            hashed_key: int,
            value: int
    ) -> None:
        self.key = key
        self.hashed_key = hashed_key
        self.value = value
        self.is_deleted = False
        self.chained_nodes_indexes = []

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(self) -> None:
        self.current_size: int = 8
        self.hash_table: list = [None] * self.current_size
        self.length = 0

    def __str__(self) -> str:
        nodes = [
            str(node)
            for node in self.hash_table
            if node and not node.is_deleted
        ]
        return (
            f"{{{', '.join(nodes)}}}"
        )

    def get_init_index(self, key: Hashable) -> int:
        return hash(key) % self.current_size

    def get_real_index(self, key: Hashable, hash_table: list) -> int:
        """Returns index of empty slot/deleted node/node with existing key"""
        index = self.get_init_index(key)
        while hash_table[index]:
            if hash_table[index].is_deleted or hash_table[index].key == key:
                break
            index = (index + 1) % self.current_size

        return index

    @staticmethod
    def set_chained_node_index(
            init_index: int,
            real_index: int,
            hash_table: list
    ) -> None:
        if init_index != real_index:
            hash_table[init_index].chained_nodes_indexes.append(
                real_index
            )

    def resize_and_rehash(self) -> None:
        self.current_size *= 2
        new_hash_table = [None] * self.current_size

        for node in self.hash_table:
            if node and not node.is_deleted:
                node_real_index = self.get_real_index(node.key, new_hash_table)
                new_hash_table[node_real_index] = Node(
                    node.key,
                    node.hashed_key,
                    node.value
                )
                self.set_chained_node_index(
                    self.get_init_index(node.key),
                    node_real_index,
                    new_hash_table
                )

        self.hash_table = new_hash_table

    def processing_existing_node(
            self,
            key: Hashable,
            value: Any,
            node: Node,
            real_index: int
    ) -> None:
        if not node.is_deleted:
            node.value = value
            return
        new_node = Node(key, hash(key), value)
        self.hash_table[real_index] = new_node
        new_node.chained_nodes_indexes = node.chained_nodes_indexes
        self.length += 1

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        real_index = self.get_real_index(key, self.hash_table)
        current_node = self.hash_table[real_index]

        if current_node:
            self.processing_existing_node(
                key,
                value,
                current_node,
                real_index
            )
            return

        if self.length + 1 > self.current_size * 2 / 3:
            self.resize_and_rehash()
            real_index = self.get_real_index(key, self.hash_table)

        self.set_chained_node_index(
            self.get_init_index(key),
            real_index,
            self.hash_table
        )

        self.hash_table[real_index] = Node(key, hash(key), value)
        self.length += 1

    def __getitem__(self, key: Hashable, deletion: bool = False) -> Any:
        node = self.hash_table[self.get_init_index(key)]

        if not node:
            raise KeyError

        if node.key == key:
            if node.is_deleted:
                raise KeyError
            else:
                return node.value if not deletion else node

        for chained_node_index in node.chained_nodes_indexes:
            chained_node = self.hash_table[chained_node_index]
            if chained_node.key == key:
                return chained_node.value if not deletion else chained_node

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * self.current_size
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        self.deleted_value = None
        node = self.__getitem__(key, deletion=True)
        node.is_deleted = True
        self.deleted_value = node.value
        self.length -= 1

    def get(self, key: Hashable, value_to_return: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return value_to_return

    def pop(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            del self[key]
            return self.deleted_value
        except KeyError:
            if default_value is not None:
                return default_value
            raise

    def update(self, other: Iterable) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> Iterator:
        self.current_index = 0
        return self

    def __next__(self) -> Node:
        while self.current_index < self.current_size:
            node = self.hash_table[self.current_index]
            self.current_index += 1
            if node and not node.is_deleted:
                return node.key
        raise StopIteration
