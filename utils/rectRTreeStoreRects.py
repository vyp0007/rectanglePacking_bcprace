from rtree import index
from rectangle import Rectangle,Position


####this version stores the rectangles directy in the rtree
class RectangleRTreeStoreRects:
    """R-tree wrapper for Rectangle objects"""
    def __init__(self):
        p = index.Property()
        p.dimension = 2
        self.idx = index.Index(properties=p)
        self._next_id = 1

    def add(self, rect: "Rectangle"):
        """Add a rectangle to the R-tree."""
        rid = self._next_id
        self._next_id += 1
        self.idx.insert(rid, (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height), obj=rect)

    def collides(self, rect: "Rectangle") -> bool:
        """Return True if rect overlaps any stored rectangle."""
        for hit in self.idx.intersection((rect.x, rect.y, rect.x + rect.width, rect.y + rect.height), objects=True):
            if hit.object.overlaps(rect):
                return True
        return False

    def findContaining(self, pos: "Position"):
        """Return a rectangle that contains the given position, or None."""
        point_bounds = (pos.x, pos.y, pos.x, pos.y)
        for hit in self.idx.intersection(point_bounds, objects=True):
            rect = hit.object
            if rect.containsPoint(pos):
                return rect
        return None

    def clear(self):
        """Reset the R-tree."""
        p = index.Property()
        p.dimension = 2
        self.idx = index.Index(properties=p)
        self._next_id = 1
