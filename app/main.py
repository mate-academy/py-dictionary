class Dictionary:
    """
    Implementação personalizada de um dicionário
    usando hash table com linear probing.

    Decisões de projeto:
    - Capacidade inicial = 8: valor pequeno, mas [
    ]uficiente para reduzir colisões no início.
    - Load factor (fator de carga) = 2/3: quando
    a tabela estiver cerca de 66% cheia,
    é feito o resize para manter a eficiência das operações.
    - Multiplicador de resize = 2: dobrar a capacidade
    garante inserções com custo amortizado O(1).
    """

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity
        self.load_factor_threshold = 2 / 3

    def _get_index(self, key: int) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node[0]] = node[2]

    def __setitem__(self, key: int, value: int) -> None:
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()

        index = self._get_index(key)
        node = self.table[index]

        if node is None:
            self.table[index] = [key, hash(key), value]
            self.size += 1
            return
        elif node[0] == key:
            self.table[index][2] = value
            return

        i = (index + 1) % self.capacity
        for _ in range(self.capacity):
            if self.table[i] is None:
                self.table[i] = [key, hash(key), value]
                self.size += 1
                return
            if self.table[i][0] == key:
                self.table[i][2] = value
                return
            i = (i + 1) % self.capacity

        raise RuntimeError("Dictionary is full even after resizing")

    def __getitem__(self, key: int) -> int:
        index = self._get_index(key)
        node = self.table[index]

        if node is None:
            raise KeyError(f"Key not found: {key}")

        if node[0] == key:
            return node[2]

        i = (index + 1) % self.capacity
        for _ in range(self.capacity):
            if self.table[i] is None:
                break
            if self.table[i][0] == key:
                return self.table[i][2]
            i = (i + 1) % self.capacity

        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size
