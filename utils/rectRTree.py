from rtree import index
from basicComponents.rectangle import Rectangle, Position

class RectangleRTree:
    """R-tree wrapper for Rectangle objects, storing rectangles in a list."""
    def __init__(self):
        p = index.Property()
        p.dimension = 2
        self.idx = index.Index(properties=p)

        self._rects = []     # stores Rectangle objects
        self._next_id = 0    # index into self._rects

    def add(self, rect: Rectangle):
        """Add a rectangle to the R-tree, storing only its index in the R-tree."""
        rid = self._next_id
        self._next_id += 1

        # Store rectangle in internal list
        self._rects.append(rect)

        # Insert bounding box with ID only (no object payload)
        bounds = (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)
        self.idx.insert(rid, bounds)

        return rid

    def collides(self, rect: Rectangle) -> bool:
        """Return True if rect overlaps any stored rectangle."""
        bounds = (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

        for rid in self.idx.intersection(bounds):
            other = self._rects[rid]
            if other.overlaps(rect):
                return True
        return False
    
    def getCollisions(self, rect : Rectangle) -> list[Rectangle]:
        """Returns list of all rectangles that collide with provided rectangle"""
        result = []
        bounds = (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

        for rid in self.idx.intersection(bounds):
            other = self._rects[rid]
            if other.overlaps(rect):
                result.append(other)
        return result
                

    def findContaining(self, pos: Position):
        """Return a rectangle that contains the given position, or None."""
        point_bounds = (pos.x, pos.y, pos.x, pos.y)

        for rid in self.idx.intersection(point_bounds):
            rect = self._rects[rid]
            if rect.containsPoint(pos):
                return rect
        return None

    def clear(self):
        """Reset the R-tree and stored rectangles."""
        p = index.Property()
        p.dimension = 2
        self.idx = index.Index(properties=p)

        self._rects = []
        self._next_id = 0
