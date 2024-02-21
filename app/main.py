class Dictionary:

    INITIAL_SIZE = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_FACTOR = 2

    def __init__(self, elements=None):
        self.size = self.INITIAL_SIZE
        self.buckets = [None] * self.size
        if elements:
            for key, value in elements:
                self.__setitem__(key, value)

    def __setitem__(self, key, value):
        hashed_value = hash(key)
        index = hashed_value % self.size
        bucket = self.buckets[index]

        try:
            eq_key = bucket[0] == key
            eq_hash = bucket[1] == hashed_value
            is_the_same_el = all([eq_key, eq_hash])
            is_collision = not eq_key

        except TypeError:
            # storing a new item
            self.check_resize()
            index = hashed_value % self.size
            self.buckets[index] = (key, hashed_value, value)

        else:
            # replacing the value for existing key
            if is_the_same_el:
                self.buckets[index] = (key, hashed_value, value)

            # dealing with collision
            if is_collision:
                self.check_resize()
                index = hashed_value % self.size
                while self.buckets[index] is not None:

                    if self.buckets[index][0] == key:
                        self.buckets[index] = (key, hashed_value, value)
                        break
                    index += 1
                    if index == self.size:
                        index = 0

                self.buckets[index] = (key, hashed_value, value)

    def check_resize(self):
        fullness = (self.size - self.buckets.count(None) + 1) / self.size
        if fullness >= self.LOAD_FACTOR:
            buckets_content = list(filter(None, self.buckets))
            self.clear()
            self.size *= self.RESIZE_FACTOR
            self.buckets = [None] * self.size
            for key, hashed_value, value in buckets_content:
                self.__setitem__(key, value)

    def __getitem__(self, key):
        hashed_value = hash(key)
        index = hashed_value % self.size
        if self.buckets[index] is None:
            raise KeyError
        while True:
            if self.buckets[index][0] == key:
                return self.buckets[index][2]
            else:
                index += 1
                if index == len(self.buckets):
                    index = 0
                if self.buckets[index] is None:
                    raise KeyError

    def __len__(self):
        return self.size - self.buckets.count(None)

    def clear(self):
        self.buckets = [None] * self.size

    def __delitem__(self, key):
        hashed_value = hash(key)
        index = hashed_value % self.size
        while True:
            if self.buckets[index][0] == key:
                self.buckets[index] = None
                break
            else:
                index += 1
                if index == len(self.buckets):
                    index = 0

    def get(self, key, def_value=None):
        hashed_value = hash(key)
        index = hashed_value % self.size

        while True:
            if self.buckets[index][0] == key:
                return self.buckets[index][2]
            else:
                index += 1
                if index == len(self.buckets):
                    index = 0
                if self.buckets[index] is None:
                    return def_value

    def pop(self, key, def_value=None):
        hashed_value = hash(key)
        index = hashed_value % self.size

        while True:
            if self.buckets[index][0] == key:
                value_to_return = self.buckets[index][2]
                self.buckets[index] = None
                return value_to_return
            else:
                index += 1
                if index == len(self.buckets):
                    index = 0
                if self.buckets[index] is None:
                    return def_value

    def update(self, to_add):
        for item_to_add in to_add:
            self.__setitem__(item_to_add[0], item_to_add[2])

    def __iter__(self):
        self.curr_ind = 0
        return self

    def __next__(self):
        while self.curr_ind < self.size:
            el = self.buckets[self.curr_ind]
            self.curr_ind += 1
            if el is not None:
                return el
        raise StopIteration
