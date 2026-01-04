from typing import Iterator


class Dictionary:
    def __init__(self) -> None:
        self.data = [None] * 8
        self.size = 8
        self.count = 0
        self.load_factor = 2 / 3

    def _hash(self, key: any) -> int:
        return hash(key) % self.size

    def _resize(self) -> None:
        self.size *= 2
        old_data = self.data
        self.data = [None] * self.size
        self.count = 0

        for node in old_data:
            if node is not None:
                self.__setitem__(node[0], node[1])

    def __setitem__(self, key: any, value: any) -> None:
        if (self.count + 1) / self.size > self.load_factor:
            self._resize()

        hash_index = self._hash(key)

        current_index = hash_index
        current_node = self.data[hash_index]

        if current_node is None:
            self.data[hash_index] = [key, value, None]
            self.count += 1
            return

        while current_node is not None:
            if current_node[0] == key:
                current_node[1] = value
                return

            if current_node[2] is None:
                break

            current_index = current_node[2]
            current_node = self.data[current_index]

        next_index = self._get_next_index()
        self.data[next_index] = [key, value, None]
        self.data[current_index][2] = next_index
        self.count += 1

    def __getitem__(self, key: any) -> any:
        hash_index = self._hash(key)

        current_node = self.data[hash_index]

        if current_node is None:
            raise KeyError(key)

        while current_node[0] != key:
            if current_node[2] is None:
                raise KeyError(key)
            current_node = self.data[current_node[2]]

        if current_node[0] != key:
            raise KeyError(key)

        return current_node[1]

    def __len__(self) -> int:
        return self.count

    def _get_next_index(self) -> int:
        for i in range(self.size):
            if self.data[i] is None:
                return i

    def __iter__(self) -> Iterator[tuple[str, any]]:
        for node in self.data:
            if node is not None:
                yield node[0], node[1]
