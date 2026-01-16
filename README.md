# Custom Dictionary Implementation

**Please note:** Before starting, make sure to read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) carefully.

## Purpose of this Task

This task is designed to challenge you to think critically about how Python's built-in data structures work behind the scenes. By implementing your own `Dictionary` class, you'll gain a deeper understanding of hash tables, memory management, and algorithmic efficiency. These are core concepts in computer science that will serve as a strong foundation for your future development as a programmer.

## Task Overview

Your goal is to create a custom `Dictionary` class that mimics the behavior of Python's built-in `dict`. You'll implement several key methods to manage key-value pairs in a way that is both efficient and robust.

### Methods to Implement

- `__setitem__(self, key, value)`  
  *This method will allow you to add or update a key-value pair in your dictionary.*

- `__getitem__(self, key)`  
  *This method will allow you to retrieve the value associated with a given key.*

- `__len__(self)`  
  *This method will return the number of key-value pairs in your dictionary.*

### Key Concepts to Consider

As you implement your custom dictionary, you'll need to keep the following concepts in mind:

- **Initial Capacity:** How much space should your dictionary allocate at the start?
- **Load Factor:** When should your dictionary resize to maintain efficiency?
- **Resize Strategy:** How should your dictionary expand its capacity when needed?

For a detailed explanation of hash tables and how they work, you can refer to this [GeeksforGeeks article on Hash Tables](https://www.geeksforgeeks.org/hash-table-data-structure/?ref=header_outind).

### Storage Structure

You'll store each key-value pair as a node in a hash table. Each node should contain the following information:
- `key`
- `hash`
- `value`

The hash table itself can be a simple list of nodes.

## Additional Features (Optional)

If you're feeling confident, you can also implement other methods that are part of the `dict` interface:

- `clear`
- `__delitem__`
- `get`
- `pop`
- `update`
- `__iter__`

These methods will help you build a more complete understanding of how dictionaries operate.

## Testing Your Dictionary

You can test your `Dictionary` class using a custom class `Point` that implements the `__hash__` and `__eq__` magic methods. This will give you practical experience with how custom objects can be used as keys in dictionaries.

**Important:** Ensure that you implement your own dictionary from scratch. Do not use Python's built-in `dict` for this task.

## Checklist

Before you push your solution, make sure to go through this [checklist](checklist.md) to ensure your code meets all the requirements.

---

By the end of this task, you'll have a solid grasp of how dictionaries work, and you'll be better prepared to tackle more complex data structures and algorithms in the future.
