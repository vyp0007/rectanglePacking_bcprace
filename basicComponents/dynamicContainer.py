from basicComponents.rectangleContainer import Container
from typing import List
import random
from utils.rectRTree import RectangleRTree
from basicComponents.rectangle import Rectangle, Position

class DynamicContainer(Container):
    def __init__(self):
        super().__init__(width=0.0)

    def add_rectangle(self, rect: "Rectangle"):
        self.rectangles.append(rect)
        self._rtree.add(rect)
        
        if rect.y + rect.height > self.height:
            self.height = rect.y + rect.height

        if rect.x + rect.width > self.width:
            self.width = rect.x + rect.width

    def canPlaceRect(self, rect: "Rectangle", pos: "Position") -> bool:
        if pos.x < 0 or pos.y < 0:
            return False

        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        
        if self._rtree.collides(test_rect):
            return False

        return True
    
    def canPlaceRect_old(self, rect: "Rectangle", pos: "Position") -> bool:
        if pos.x < 0 or pos.y < 0:
            return False
        
        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        
        for other in self.rectangles:
            if other.overlaps(test_rect):
                return False
        return True
    
    def testRectanglePlacement(self,rectangle : Rectangle, position : Position) -> tuple[float,float]:
        """tests how the dimension of the dynamic container would change if the provided rectangle was placed on the provided position
            Returns tuple (width, height)
        """
        return (max(self.width,rectangle.width + position.x),max(self.height,rectangle.height + position.y))