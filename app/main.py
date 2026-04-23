from typing import Any, Optional


class Dictionary:
    def __init__(self) -> None:
        self.table: list[Optional[list[tuple[Any, int, Any]]]] = [None] * 8
        self.size: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % len(self.table)

        if self.table[index] is None:
            self.table[index] = [(key, key_hash, value)]
            self.size += 1
        else:
            bucket = self.table[index]

            for i, (k, h, v) in enumerate(bucket):
                if h == key_hash and k == key:
                    bucket[i] = (key, key_hash, value)
                    return

            bucket.append((key, key_hash, value))
            self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self.table)

        bucket = self.table[index]
        if bucket is not None:
            for k, h, v in bucket:
                if h == key_hash and k == key:
                    return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
