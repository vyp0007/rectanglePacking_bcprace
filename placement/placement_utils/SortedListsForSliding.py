from sortedcontainers import SortedList
from typing import Iterator
from basicComponents.rectangle import Rectangle

class RectangleSortedList:
    def __init__(self):
        self.by_right = SortedList(key=lambda r: r.x + r.width)
        self.by_left = SortedList(key=lambda r: r.x)
        self.by_top = SortedList(key=lambda r: r.y + r.height)
        self.by_bottom = SortedList(key=lambda r: r.y)


    def add(self, rect):
        self.by_right.add(rect)
        self.by_top.add(rect)
        self.by_bottom.add(rect)
        self.by_left.add(rect)

    def remove(self, rect):
        self.by_right.remove(rect)
        self.by_top.remove(rect)
        self.by_bottom.remove(rect)
        self.by_left.remove(rect)

    def iter_right_desc(self) -> Iterator[Rectangle]:
        return reversed(self.by_right)

    def iter_top_desc(self) -> Iterator[Rectangle]:
        return reversed(self.by_top)