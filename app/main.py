class Node:
    def __init__(self, key: int | float, value: int | float) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 16,
            load_factor: float = 0.75
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.capacity = initial_capacity
        self.table = [None] * initial_capacity

    def __hash_func(self, key: int | float) -> int:
        return hash(key) % self.capacity

    def __resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity
        for node in self.table:
            while node:
                index = self.__hash_func(node.key)
                next_node = node.next
                node.next = new_table[index]
                new_table[index] = node
                node = next_node
        self.table = new_table

    def __setitem__(
            self,
            key: int | float | None,
            value: int | float | None
    ) -> int or None:
        index = self.__hash_func(key)
        new_node = Node(key, value)
        if self.table[index] is None:
            self.table[index] = new_node
        else:
            current_node = self.table[index]
            while current_node:
                if current_node.key == key:
                    current_node.value = value
                    return
                if current_node.next is None:
                    break
                current_node = current_node.next
            current_node.next = new_node
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self.__resize()

    def __getitem__(self, key: int | float) -> int | float:
        index = self.__hash_func(key)
        current_node = self.table[index]
        while current_node:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
