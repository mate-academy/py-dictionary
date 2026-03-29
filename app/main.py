OBJ_DICT = object()


class Dictionary:
    def __init__(self):
        self.size_table = 8
        self.memory_cell = [None] * self.size_table
        self.length_memory_cell = 0

    def __setitem__(self, key, value):
        if self.check_table_size():
            self.resize_table()

        self.fill_in_table_cells(self.memory_cell, key, value)

    def __getitem__(self, item):
        index_hash = self.get_hash_index(item)

        while self.memory_cell[index_hash] is not None:
            if self.memory_cell[index_hash] is not OBJ_DICT:
                key_cell, hash_cell, value_cell = self.memory_cell[index_hash]
                if key_cell == item:
                    return value_cell
                index_hash = (index_hash + 1) % self.size_table
        else:
            raise KeyError

    def __len__(self):
        return self.length_memory_cell

    @property
    def table_hash(self):
        table_hash_ = []
        for cell_ in self.memory_cell:
            if cell_ not in (None, OBJ_DICT):
                key, _, value = cell_
                table_hash_.append((key, value))
        return table_hash_

    def get_hash_index(self, key):
        hashed_key = hash(key)
        index = hashed_key % self.size_table
        return index

    def check_table_size(self):
        threshold = int(2 / 3 * self.size_table)
        if self.length_memory_cell >= threshold:
            self.size_table *= 2
            return True
        return False

    def resize_table(self):
        new_cells = [None] * self.size_table
        for cell in self.memory_cell:
            if cell not in (None, OBJ_DICT):
                key, _, value = cell
                self.fill_in_table_cells(new_cells, key, value)
                self.length_memory_cell -= 1

        self.memory_cell = new_cells

    def fill_in_table_cells(self, cell, key, value):
        hash_index = self.get_hash_index(key)

        while cell[hash_index] is not None:
            if cell[hash_index] is OBJ_DICT:
                cell[hash_index] = (key, hash(key), value)

            cell_key, cell_hash, cell_value = cell[hash_index]
            if cell_key == key:
                cell[hash_index] = cell_key, cell_hash, value
                self.length_memory_cell -= 1
                break
            else:
                hash_index = (hash_index + 1) % self.size_table

        cell[hash_index] = (key, hash(key), value)
        self.length_memory_cell += 1
