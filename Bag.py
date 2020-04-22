class Bag:

    def __init__(self, _items=None):
        self._items = _items if _items else []
        self._size = len(_items) if _items else 0

    def get_size(self):
        return self._size

    def add(self, item):
        self._items.append(item)
        self._size += 1

    def __iter__(self):
        yield from self._items

    def is_empty(self):
        return self._size == 0

    def __getitem__(self, idx):
        return self._items[idx]
