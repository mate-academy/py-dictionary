from typing import Any, Iterator, Tuple


class Dictionary:
    def __init__(self) -> None:
        """
        capacity = initial capacity of dictionary,
        loadFactor = occupancy rate
        threshold = maximum occupancy
        blocks = dict memory block
        order = blocks order
        count = count of active blocks
        """
        self.capacity = 8
        self.loadFactor = 0.66
        self.threshold = int(self.capacity * self.loadFactor)

        self.blocks = [[] for _ in range(self.capacity)]
        self.order = []
        self.count = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        key_hash = searching hash of key
        key_block = searching block for saving
        block_status_option: ["Alive", "Dead"]
            "Alive" -> active block
            "Dead" -> block was removed
        block_value: values from block

        if len(self.order) >= self.threshold:
        when filled blocks count equal to our maximum occupancy,
        we update our capacity

        for i in range(self.capacity):
        We search key block in our blocks.
        If hash works correct we will save our value at first iteration,
        else until find empty or dead block
        """
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError("Key must be hashable!")

        if self.count >= self.threshold:
            self.__resize()

        for i in range(self.capacity):
            index = (key_hash + i) % self.capacity
            block = self.blocks[index]

            if not block or block[-1] == "Dead":
                self.blocks[index] = [key_hash, key, value, "Alive"]
                self.order.append(key)
                self.count += 1
                return

            if block[0] == key_hash and block[1] == key:
                self.blocks[index] = [key_hash, key, value, "Alive"]
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

            status = block[-1]

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
            if not block or block[-1] == "Dead":
                continue

            key_hash = block[0]
            key = block[1]
            value = block[2]

            for i in range(self.capacity):
                index = (key_hash + i) % self.capacity

                target_slot = self.blocks[index]

                if not target_slot or target_slot[-1] == "Dead":
                    self.blocks[index] = [key_hash, key, value, "Alive"]
                    self.count += 1
                    break

    def __len__(self) -> int:
        return len(self.order)

    def __str__(self) -> str:
        parts = []

        for key in self.order:
            repr_value = repr(self.__getitem__(key))
            current_key = repr(key)
            parts.append(f"{current_key}: {repr_value}")

        return "{" + ", ".join(parts) + "}"

    def clear(self) -> None:
        self.blocks = [[] for _ in range(self.capacity)]
        self.order = []

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

            if block[-1] == "Dead":
                continue

            if block[0] == key_hash and block[1] == key:
                self.blocks[index] = [key_hash, None, None, "Dead"]
                self.order.remove(key)
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
        return iter(self.order)

    def items(self) -> Iterator[Tuple[Any, Any]]:
        for key in self.order:
            yield key, self.__getitem__(key)

    def keys(self) -> list:
        return list(self.order)
