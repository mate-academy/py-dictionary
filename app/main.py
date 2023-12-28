class Node:
    def __init__(self,
                 key: any,
                 hash_code: int,
                 value: any
                 ) -> None:
        self.key: any = key
        self.hash_code: int = hash_code
        self.value: any = value
        self.next: Node | None = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 0.666
        self.size: int = 0
        self.table: list[Node | None] = [None] * 8

    def __repr__(self) -> str:
        items = ", ".join(f"{node.key}: {node.value}"
                          for node in self.table
                          if node)
        return "{" + items + "}"

    def __setitem__(self,
                    key: any,
                    value: any
                    ) -> None:
        hash_code: int = hash(key)
        index: int = hash_code % self.capacity

        current_node: Node | None = self.table[index]
        while current_node:
            if current_node.key == key:
                current_node.value = value
                return
            current_node = current_node.next

        new_node: Node = Node(key, hash_code, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1
        self._check_resize()

    def __getitem__(self, key: any) -> any:
        hash_value = hash(key)
        current: Node | None = self.table[hash_value % self.capacity]

        while current:
            if current.key == key and current.hash_code == hash_value:
                return current.value
            current = current.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: any) -> None:
        index: int = hash(key) % self.capacity
        current: Node | None = self.table[index]
        previous: Node | None = None

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

    def get(self, key: any) -> any:
        return self[key]

    def pop(self, key: any) -> any:
        value: any = self[key]
        del self[key]
        return value

    def update(self, new: dict) -> None:
        for key, value in new.items():
            self[key] = value

    def __iter__(self) -> any:
        for node in self.table:
            while node:
                yield node.key
                node = node.next

    def clear(self) -> None:
        self.__init__()

    def _check_resize(self) -> None:
        if self.size / self.capacity > self.load_factor:
            new_capacity: int = self.capacity * 2
            new_table: list[Node | None] = [None] * new_capacity

            for node in self:
                if isinstance(node, Node):
                    new_index: int = node.hash_code % new_capacity
                    new_node: Node = Node(node.key, node.hash_code, node.value)
                else:
                    new_index: int = hash(node) % new_capacity
                    new_node: Node = Node(node, hash(node), self[node])

                new_node.next = new_table[new_index]
                new_table[new_index] = new_node

            self.capacity = new_capacity
            self.table = new_table
