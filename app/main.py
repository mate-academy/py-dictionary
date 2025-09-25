from typing import Any


class Dictionary:


    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.75
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _index_for(self, h: int) -> int:
        return h % self.capacity


    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: int) -> Any:
        h = hash(key)
        i = self._index_for(h)
        if i not in self.buckets[i]:


    def __setitem__(self, key: int, value: Any) -> None:
        h = hash(key)




    def find_bucket_entry(self, h: int, key: int, value: int) -> Any:












