class Dictionary:
    def __init__(self) -> None:
        self.table = [None] * 5
        self.size = 0

    def resize(self) -> None:
        old_table = self.table

        # збільшуємо таблицю вдвічі
        self.table = [None] * (len(old_table) * 2)

        # обнуляємо size, бо будемо додавати елементи заново
        old_size = self.size
        self.size = 0

        # переносимо всі елементи
        for bucket in old_table:
            if bucket is not None:
                for key, value in bucket:
                    self[key] = value

        self.size = old_size

    def __setitem__(self, key: int, value: int) -> None:
        # якщо таблиця заповнена більше ніж на 70%
        if self.size / len(self.table) > 0.7:
            self.resize()

        index = hash(key) % len(self.table)

        if self.table[index] is None:
            self.table[index] = []

        # оновлення існуючого ключа
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return

        # додавання нового ключа
        self.table[index].append([key, value])
        self.size += 1

    def __getitem__(self, key: int) -> None:
        index = hash(key) % len(self.table)

        if self.table[index] is None:
            raise KeyError(key)

        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]

        raise KeyError(key)

    def __len__(self) -> None:
        return self.size
