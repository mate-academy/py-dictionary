from collections.abc import Hashable
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.bucket = [None] * 8
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        i = hash(key) % len(self.bucket)

        if not self.bucket[i]:
            self.bucket[i] = [(key, hash(key), value)]
            self.length += 1
            if self.length / len(self.bucket) >= 0.75:
                self._resize()
        else:
            for index, node in enumerate(self.bucket[i]):
                if node[0] == key:
                    self.bucket[i][index] = ((key, hash(key), value))
                    break
            else:
                self.bucket[i].append((key, hash(key), value))
                self.length += 1
                if self.length / len(self.bucket) >= 0.75:
                    self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        i = hash(key) % len(self.bucket)
        if not self.bucket[i]:
            raise KeyError(f"Key not found: {key}")
        for node in self.bucket[i]:
            if node[0] == key:
                return node[2]
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_bucket = self.bucket
        self.bucket = [None] * len(old_bucket) * 2
        self.length = 0
        for cell in old_bucket:
            if cell:
                for node in cell:
                    self[node[0]] = node[2]
