class Dictionary:

    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_FACTOR = 2

    def __init__(self):
        self.elements = [None for _ in range(self.INITIAL_CAPACITY)]
        self.size = 0
        self.capacity = self.INITIAL_CAPACITY

    def resize(self):
        current_elements = [node for node in self.elements if node is not None]
        self.capacity *= self.RESIZE_FACTOR
        self.elements = [None for _ in range(self.capacity)]
        self.size = 0
        for node in current_elements:
            self.__setitem__(node[0], node[1])

    def __setitem__(self, key, value):

        if (self.size + 1) > self.capacity * self.LOAD_FACTOR:
            self.resize()

        hash_ = hash(key)
        index = hash_ % len(self.elements)
        node = [key, value, hash_]

        while self.elements[index] is not None:
            if self.elements[index][2] == hash_ \
                    and self.elements[index][0] == key:
                self.elements[index][1] = value
                return
            index = (index + 1) % len(self.elements)

        self.elements[index] = node
        self.size += 1

    def __getitem__(self, item):
        hash_ = hash(item)
        index = hash_ % len(self.elements)

        while self.elements[index] is not None:
            if self.elements[index][2] == hash_ \
                    and self.elements[index][0] == item:
                return self.elements[index][1]

            index = (index + 1) % len(self.elements)

        raise KeyError(f"Key {item} does not exist")

    def __repr__(self):
        return str(self.elements)

    def __len__(self):
        return self.size
