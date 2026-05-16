from typing import Generator


TOMBSTONE = object()


class Dictionary:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.length = 0
        self.hash_table = [None] * self.size

    def _index(self, key_hash: int) -> int:
        return key_hash & (self.size - 1)

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.size *= 2
        self.hash_table = [None] * self.size
        self.length = 0

        for slot in old_hash_table:
            if slot is not None and slot is not TOMBSTONE:
                key, _, value = slot
                self[key] = value

    def _probe(self, key_hash: int) -> Generator[int, None, None]:
        index = self._index(key_hash)
        perturb = key_hash

        while True:
            yield index
            index = (index * 5 + 1 + perturb) & (self.size - 1)
            perturb >>= 5

    def __setitem__(self, key: any, value: any) -> None:
        if self.length * 3 >= self.size * 2:
            self._resize()

        key_hash = hash(key)

        for index in self._probe(key_hash):
            slot = self.hash_table[index]
            if slot is None or slot is TOMBSTONE:
                self.hash_table[index] = (key, key_hash, value)
                self.length += 1
                return
            if slot[0] == key and slot[1] == key_hash:
                self.hash_table[index] = (key, key_hash, value)
                return

    def __getitem__(self, key: any) -> any:
        key_hash = hash(key)

        for index in self._probe(key_hash):
            slot = self.hash_table[index]

            if slot is None:
                raise KeyError(f"Error: {key} does not exist.")

            if slot is not TOMBSTONE:
                if slot[0] == key and slot[1] == key_hash:
                    return slot[2]

    def __delitem__(self, key: any) -> None:
        key_hash = hash(key)

        for index in self._probe(key_hash):
            slot = self.hash_table[index]

            if slot is None:
                raise KeyError(f"Error: {key} does not exist.")

            if slot is not TOMBSTONE:
                if slot[0] == key and slot[1] == key_hash:
                    self.hash_table[index] = TOMBSTONE
                    self.length -= 1
                    return

    def __len__(self) -> int:
        return self.length
