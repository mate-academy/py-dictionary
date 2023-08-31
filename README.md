# Custom dict

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before starting.

Let's create your own class `Dictionary` and implement methods:
- `__setitem__(self, key, value)` 
- `__getitem__(self, key)` 
- `__len__(self)`

Be attentive to basic requirements for the implementation of the dictionary (initial capacity, load factor, resize ...)

Also, don't forget to store `(key, hash, value)` as a node in the hash table. A hash table may be stored as a simple list of nodes.

**Notes**: 
- You can implement other methods of the dict interface (both regular and magic):
  - `clear`
  - `__delitem__`
  - `get`
  - `pop`
  - `update`
  - `__iter__`
- you can test `Dictionary` with custom class `Point` that has `__hash__` and `__eq__` magic methods;
- **You should implement your own custom dictionary, do not use built-in `dict` for this task**.

### Note: Check your code using this [checklist](checklist.md) before pushing your solution.
