from typing import Any, Iterator, Tuple


class OrderNode:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.prev = self
        self.next = self


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.loadFactor = 0.66
        self.threshold = int(self.capacity * self.loadFactor)
        self.blocks = [[] for _ in range(self.capacity)]

        self.root = OrderNode(None)
        self.count = 0

    def __order_append(self, key: Any) -> OrderNode:
        new_node = OrderNode(key)

        last = self.root.prev
        root = self.root

        new_node.prev = last
        new_node.next = root

        last.next = new_node
        root.prev = new_node

        return new_node

    def __order_delete(self, node: OrderNode) -> None:
        if node is not self.root:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = None
            node.next = None

    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError("Key must be hashable!")

        if self.count >= self.threshold:
            self.__resize()

        for i in range(self.capacity):
            index = (key_hash + i) % self.capacity
            block = self.blocks[index]
            if not block or block[3] == "Dead":
                new_node = self.__order_append(key)
                self.blocks[index] = [key_hash, key, value, "Alive", new_node]
                self.count += 1
                return

            if block[0] == key_hash and block[1] == key:
                node = block[4]
                self.blocks[index] = [key_hash, key, value, "Alive", node]
                return

    def __getitem__(self, key: Any) -> Any:
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError("Key must be hashable!")

        for i in range(self.capacity):
            index = (key_hash + i) % self.capacity
            block = self.blocks[index]

            if not block:
                raise KeyError("Key not exist")

            status = block[3]

            if status == "Dead":
                continue

            if block[0] == key_hash and block[1] == key:
                return block[2]

        raise KeyError("Key not exist!")

    def __resize(self) -> None:
        previous_blocks = self.blocks

        self.capacity *= 2
        self.threshold = int(self.capacity * self.loadFactor)
        self.blocks = [[] for _ in range(self.capacity)]
        self.count = 0

        for block in previous_blocks:
            if not block or block[3] == "Dead":
                continue

            key_hash = block[0]
            key = block[1]
            value = block[2]
            node = block[4]

            for i in range(self.capacity):
                index = (key_hash + i) % self.capacity

                target_slot = self.blocks[index]

                if not target_slot or target_slot[3] == "Dead":
                    self.blocks[index] = [key_hash, key, value, "Alive", node]
                    self.count += 1
                    break

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        parts = []
        for key in self:
            repr_value = repr(self.__getitem__(key))
            current_key = repr(key)
            parts.append(f"{current_key}: {repr_value}")

        return "{" + ", ".join(parts) + "}"

    def clear(self) -> None:
        self.blocks = [[] for _ in range(self.capacity)]
        self.root = OrderNode(None)
        self.count = 0

    def __delitem__(self, key: Any) -> None:
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError("Key must be hashable!")
        for i in range(self.capacity):
            index = (key_hash + i) % self.capacity
            block = self.blocks[index]

            if not block:
                break

            if block[3] == "Dead":
                continue

            if block[0] == key_hash and block[1] == key:
                node_to_delete = block[4]
                self.__order_delete(node_to_delete)

                self.blocks[index] = [
                    key_hash,
                    None,
                    None,
                    "Dead",
                    node_to_delete
                ]
                self.count -= 1
                return

        raise KeyError("Key not exist")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            if default is None:
                raise KeyError("Key not exist!")
            return default

        self.__delitem__(key)
        return value

    def update(self, other: Any) -> None:
        if hasattr(other, "items"):
            iterable = other.items()
        elif hasattr(other, "keys"):
            try:
                iterable = [(key, other[key]) for key in other]
            except (TypeError, KeyError):
                raise TypeError("Expected a mapping with key-value access")
        elif hasattr(other, "__iter__"):
            iterable = other
        else:
            raise TypeError("Object is not iterable")

        for item in iterable:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                raise ValueError("Object must contain at least 2 items!")

            key, value = item
            self.__setitem__(key, value)

    def __iter__(self) -> Iterator[Any]:
        current = self.root.next
        while current is not self.root:
            yield current.key
            current = current.next

    def items(self) -> Iterator[Tuple[Any, Any]]:
        current = self.root.next
        while current is not self.root:
            yield current.key, self.__getitem__(current.key)
            current = current.next

    def keys(self) -> list:
        return list(self.__iter__())
