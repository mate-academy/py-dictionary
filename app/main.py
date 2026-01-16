class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.basket = [None] * self.size
        self.count = 0
        self.load = 2 / 3

    def __setitem__(self, key: int, value: any) -> None:

        if isinstance(key, (list, dict, set)) or not key:
            raise KeyError("key must be immutable")
        if value is None:
            raise ValueError("value is empty")

        if self.count >= self.size * self.load:
            self.__resize__()

        index = hash(key) % self.size

        while self.basket[index] is not None:
            if self.basket[index][0] == key:
                self.basket[index][1] = value
                return
            index = (index + 1) % self.size

        self.basket[index] = [key, value]
        self.count += 1

    def __getitem__(self, key: int) -> any:

        index = hash(key) % self.size
        counter = 0

        while self.basket[index] is not None:
            if self.basket[index][0] == key:
                return self.basket[index][1]
            index = (index + 1) % self.size
            counter += 1
            if counter == self.size:
                break
        raise KeyError("Key is missed")

    def __len__(self) -> int:
        return self.count

    def __resize__(self) -> None:
        old_basket = self.basket
        self.size = self.size * 2
        self.basket = [None] * self.size
        self.count = 0
        for bk in old_basket:
            if bk is not None:
                self.__setitem__(bk[0], bk[1])
