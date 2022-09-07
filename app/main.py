class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE = 2

    class Node:
        def __init__(self, key, value, key_hash):
            self.key = key
            self.value = value
            self.key_hash = key_hash

    def __init__(self):
        self.container = [None] * self.INITIAL_CAPACITY
        self.elements = 0
        self.length = len(self.container)

    def resize(self):
        old_container = self.container
        self.INITIAL_CAPACITY *= self.RESIZE
        self.container = [None] * self.INITIAL_CAPACITY
        self.length *= 2
        self.elements = 0
        for cell in old_container:
            if cell:
                self.__setitem__(cell.key, cell.value)

    def __setitem__(self, key, value):
        key_hash = hash(key)
        index = key_hash % self.length

        if self.elements == round(self.length * self.LOAD_FACTOR):
            self.resize()

        if not self.container[index]:
            self.container[index] = self.Node(key, value, key_hash)
            self.elements += 1

        elif self.container[index].key_hash == key_hash and \
                self.container[index].key == key:
            self.container[index].value = value

        else:
            index = (index + 1) % self.length
            while True:
                if not self.container[index]:
                    self.container[index] = self.Node(key, value, key_hash)
                    self.elements += 1
                    break
                elif self.container[index].key == key:
                    self.container[index].value = value
                    break
                index = (index + 1) % self.length

    def __getitem__(self, key):
        key_hash = hash(key)
        index = key_hash % self.length
        while self.container[index] is not None:
            if self.container[index].key_hash == key_hash \
                    and self.container[index].key == key:
                return self.container[index].value
            index = (index + 1) % self.length
        raise KeyError

    def __len__(self):
        return self.elements
