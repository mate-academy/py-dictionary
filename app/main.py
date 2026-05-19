class Dictionary:
    def __init__(self) -> None:
        self._size = 8
        self._count = 0
        self._table = [None] * self._size

    def __setitem__(self, key: object, value: object) -> None:
        hashcode = hash(key)
        if self._count + 1 > self._size * 2 / 3:
            self._resize(self._size * 2)

        index = self._index_for_hash(hashcode)
        bucket = self._table[index]
        if bucket is None:
            self._table[index] = [(key, hashcode, value)]
            self._count += 1
            return

        for item_index, (existing_key, existing_hash, _) in enumerate(bucket):
            if existing_hash == hashcode and existing_key == key:
                bucket[item_index] = (existing_key, existing_hash, value)
                return

        bucket.append((key, hashcode, value))
        self._count += 1

    def __getitem__(self, key: object) -> object:
        hashcode = hash(key)
        bucket = self._table[self._index_for_hash(hashcode)]
        if bucket is None:
            raise KeyError(key)

        for existing_key, existing_hash, value in bucket:
            if existing_hash == hashcode and existing_key == key:
                return value

        raise KeyError(key)

    def __len__(self) -> int:
        return self._count

    def _index_for_hash(self, hashcode: int) -> int:
        return hashcode % self._size

    def _resize(self, new_size: int) -> None:
        old_table = self._table
        self._size = new_size
        self._table = [None] * self._size
        self._count = 0

        for bucket in old_table:
            if bucket is None:
                continue
            for key, hashcode, value in bucket:
                self._insert_existing(key, hashcode, value)

    def _insert_existing(
        self, key: object, hashcode: int, value: object
    ) -> None:
        index = self._index_for_hash(hashcode)
        bucket = self._table[index]
        if bucket is None:
            self._table[index] = [(key, hashcode, value)]
        else:
            bucket.append((key, hashcode, value))
        self._count += 1
