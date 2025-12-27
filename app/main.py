from typing import Optional, List


class Node:
    def __init__(self, key: object, value: object) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.load_factor = load_factor
        self.capacity = capacity
        self.table = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        self._extend_table()

        hash_key = hash(key)
        cell_index = hash_key % self.capacity

        current_cell = self.table[cell_index]

        if current_cell is None:
            self.table[cell_index] = [Node(key, value)]
        else:
            self._handle_collision(cell_index, Node(key, value), update=True)

    def _handle_collision(
            self,
            cell_index: int,
            new_item: Node,
            update: bool = False
    ) -> None:
        current_cell = self.table[cell_index]

        if isinstance(current_cell, list):
            for i, node in enumerate(current_cell):
                if update and node.key == new_item.key:
                    current_cell[i] = new_item
                    return
            current_cell.append(new_item)
        else:
            raise TypeError("Collision occurred, but current"
                            " cell structure is unexpected.")

    def __getitem__(self, key: object) -> object:
        hash_key = hash(key)
        cell_index = hash_key % self.capacity

        current_cell = self.table[cell_index]

        if current_cell is not None:
            for node in current_cell:
                if node.key == key:
                    return node.value

        raise KeyError(f"Key: {key} doesn't exist in table")

    def _extend_table(self) -> None:
        if self._load_factor_exceeded():
            self._resize_table()

    def _load_factor_exceeded(self) -> bool:
        occupied_cells = sum(1 for cell in self.table if cell is not None)
        return occupied_cells >= self.load_factor * self.capacity

    def _resize_table(self) -> None:
        new_capacity = self.capacity * 2
        new_table: List[Optional[List[Node]]] = [None] * new_capacity

        for cell in self.table:
            if cell is not None:
                self._rehash_cell(cell, new_table)

        self.capacity = new_capacity
        self.table = new_table

    @staticmethod
    def _rehash_cell(
            cell: List[Node],
            new_table: List[Optional[List[Node]]]
    ) -> None:
        for node in cell:
            hash_key = node.hash
            cell_index = hash_key % len(new_table)

            if new_table[cell_index] is None:
                new_table[cell_index] = [node]
            else:
                new_table[cell_index].append(node)

    def __len__(self) -> int:
        count = 0
        for cell in self.table:
            if cell is not None:
                count += len(cell)
        return count

    def clear(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
