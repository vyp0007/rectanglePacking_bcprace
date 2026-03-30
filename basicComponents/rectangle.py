import random

class Position:

    _next_id = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self._id = Position._next_id
        Position._next_id += 1

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, id:{self._id}"

    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    


class Rectangle:
    def __init__(self, width: float, height: float, x: float = None, y: float = None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = self.random_color()

    @staticmethod
    def random_color():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def overlaps(self, other: "Rectangle") -> bool:
        """
        Returns True if rectangles overlap.
        Sharing an edge is NOT considered overlapping.
        """
        return not (
            self.x + self.width <= other.x or  
            self.x >= other.x + other.width or  
            self.y + self.height <= other.y or  
            self.y >= other.y + other.height  
        )

    def containsPoint(self, pos: Position) -> bool:
        """
        Returns True if the rectangle contains the point.
        """
        if self.x is None or self.y is None:
            return False

        return (self.x <= pos.x < self.x + self.width and
                self.y <= pos.y < self.y + self.height)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}"
    
    def setPosition(self, position : Position):
        self.x = position.x
        self.y = position.y
    
    @property
    def bounds(self):
        """Return (xmin, ymin, xmax, ymax) for use in Rtree."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
