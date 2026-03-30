import bisect

class UniqueOrderedList:
    def __init__(self):
        self._items = []

    def add(self, item):
        # Use binary search to find insertion point
        i = bisect.bisect_left(self._items, item)
        if i == len(self._items) or self._items[i] != item:
            self._items.insert(i, item)  # Keep sorted

    def __contains__(self, item):
        i = bisect.bisect_left(self._items, item)
        return i != len(self._items) and self._items[i] == item

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __repr__(self):
        return repr(self._items)
