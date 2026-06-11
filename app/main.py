from typing import Any


class Dictionary:
    # --- CLASSE INTERNE ---
    class Node:
        # La clé peut être de n'importe quel type hashable (Any)
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

        def __repr__(self) -> str:
            return f"Node({self.key}: {self.value})"
    # ----------------------

    def __init__(self) -> None:
        self.capacity = 8
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    # CORRECTION : Renvoie un entier, pas None !
    def _get_bucket_index(self, key: Any) -> int:
        return hash(key) & (self.capacity - 1)

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.size + 1) / self.capacity > 2 / 3:
            self._resize()

        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        new_node = self.Node(key, value)
        bucket.append(new_node)
        self.size += 1

    # CORRECTION : Renvoie n'importe quel type de valeur stockée (Any)
    def __getitem__(self, key: Any) -> Any:
        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets

        if self.capacity < 50000:
            self.capacity *= 4
        else:
            self.capacity *= 2

        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self.__setitem__(node.key, node.value)
