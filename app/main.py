from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.dict_capacity = 8
        self.load_factor = int(self.dict_capacity * (2 / 3))
        self.dict_data = [False for _ in range(8)]
        self.dict_len = 0
        self.free_paces_in_dict_data = [i for i in range(self.dict_capacity)]
        self.need_to_extend = False

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index_to_write = key_hash % self.dict_capacity

        if not self.dict_data[index_to_write]:
            self.dict_data[index_to_write] = (key_hash, key, value)
            self.free_paces_in_dict_data.remove(index_to_write)
            self.dict_len += 1

        elif self.dict_data[index_to_write]:
            item_hash, item_key, item_value = self.dict_data[index_to_write]

            if item_hash == hash(key) and item_key == key:
                self.dict_data[index_to_write] = (item_hash, item_key, value)
            else:
                need_to_continue = True

                for i, item in enumerate(self.dict_data):
                    if item:
                        sec_item_hash, sec_item_key, sec_item_value = item
                        if sec_item_hash == key_hash and sec_item_key == key:
                            self.dict_data[i] = (sec_item_hash,
                                                 sec_item_key,
                                                 value)
                            need_to_continue = False
                            break

                if need_to_continue:
                    temp_index = self.free_paces_in_dict_data[0]
                    self.dict_data[temp_index] = (key_hash, key, value)
                    self.free_paces_in_dict_data.remove(temp_index)
                    self.dict_len += 1

        self.check_load_factor()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.dict_capacity

        if not self.dict_data[index]:
            raise KeyError

        data_hash, data_key, data_value = self.dict_data[index]

        if key == data_key:
            return data_value

        for i, data_item in enumerate(item for item in self.dict_data if item):
            data_item_hash, data_item_key, data_item_value = data_item
            if data_item_key == key:
                return data_item_value

    def __len__(self) -> int:
        return self.dict_len

    def check_load_factor(self) -> None:
        if self.dict_len == self.load_factor:
            self.need_to_extend = True
            self.__resize__()

    def __resize__(self) -> None:
        self.dict_capacity *= 2
        self.load_factor = int(self.dict_capacity * (2 / 3))
        self.free_paces_in_dict_data = [_ for _ in range(self.dict_capacity)]
        self.dict_len = 0
        only_true_dict_data = [item for item in self.dict_data if item]
        self.dict_data = [False for _ in range(self.dict_capacity)]

        for item in only_true_dict_data:
            item_hash, item_key, item_value = item
            self.__setitem__(item_key, item_value)
            self.need_to_extend = False
