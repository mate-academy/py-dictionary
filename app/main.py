class Dictionary:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__table = [[] for _ in range(size)]

    def hashfunction(self, key: object):
        return hash(key) % self.__size

    def __setitem__(self, key: object, value: object):
        index = self.hashfunction(key)
        bucket = self.__table[index]
        for item, (k, v) in enumerate(bucket):
            if k == key:
                bucket[item] = (key, value)
                return
        bucket.append((key, value))

    def __getitem__(self, key: object):
        index = self.hashfunction(key)
        bucket = self.__table[index]
        for k, v in bucket:
            if k == key:
                 return v

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self.__table)
