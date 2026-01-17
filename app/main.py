from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.capacity = len(self.hash_table)
        self.length = 0
        self.load_factor_threshold = 0.75

    def node(
        self,
        key: Any,
        hash_num: int,
        value: Any
    ) -> tuple[Any, int, Any]:
        return key, hash_num, value

    def aux_cal(self, key: Any) -> tuple[int, int]:
        compute_hash = hash(key)
        index = compute_hash % self.capacity
        return compute_hash, index

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for bucket in self.hash_table:
            if bucket is None:
                continue
            for node in bucket:
                node_hash = node[1]
                new_index = node_hash % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = [node]
                else:
                    new_table[new_index].append(node)
        self.hash_table = new_table
        self.capacity = new_capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        compute_hash, index = self.aux_cal(key)
        bucket = self.hash_table[index]
        if bucket is None:
            self.hash_table[index] = [self.node(key, compute_hash, value)]
            self.length += 1
        else:
            for i, node in enumerate(bucket):
                node_key = node[0]
                if node_key == key:
                    bucket[i] = self.node(key, node[1], value)
                    return
            bucket.append(self.node(key, compute_hash, value))
            self.length += 1
        if self.length / self.capacity > self.load_factor_threshold:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        compute_hash, index = self.aux_cal(key)

        if self.hash_table[index] is not None:
            for node in self.hash_table[index]:
                if node[0] == key:
                    return node[2]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
