from typing import List
import random
from utils.rectRTree import RectangleRTree
from basicComponents.rectangle import Rectangle, Position
#from utils.rectRTreeStoreRects import RectangleRTreeStoreRects


class Container:
    def __init__(self, width: float):
        self.width = width
        self.rectangles: List["Rectangle"] = []
        self.height: float = 0.0
        self._rtree = RectangleRTree()

    def add_rectangle(self, rect: "Rectangle"):
        self.rectangles.append(rect)
        self._rtree.add(rect)  #add to rtree
        if rect.y + rect.height > self.height:
            self.height = rect.y + rect.height

    def add_rectangles(self, rects: list["Rectangle"]):
        for r in rects:
            self.add_rectangle(r)

    def canPlaceRect(self, rect: "Rectangle", pos: "Position") -> bool:
        """
        Checks if the rectangle can be placed at the position without overlapping others,
        and within container bounds.
        """
        #check container bounds
        if rect.width + pos.x > self.width or pos.x < 0 or pos.y < 0:
            return False

        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        #uses rtree
        if self._rtree.collides(test_rect):
            return False

        return True
    
    def canPlaceRect_old(self, rect: "Rectangle", pos: "Position") -> bool:
        if rect.width + pos.x > self.width or pos.x < 0 or pos.y < 0:
            return False
        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        for other in self.rectangles:
            if other.overlaps(test_rect):
                return False
        return True
    
    def getCollidingRectangles(self, rect: "Rectangle", pos: "Position"):
        """returns a list of rectangles that would collide with the provided rectangle on provided position"""
        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        return self._rtree.getCollisions(test_rect)
    
    def getCollidingRectangles_old(self, rect: "Rectangle", pos: "Position"):
        """returns a list of rectangles that would collide with the provided rectangle on provided position
        , uses brute force to check for collisions"""
        test_rect = Rectangle(rect.width, rect.height, pos.x, pos.y)
        collisions = []
        for other in self.rectangles:
            if other.overlaps(test_rect):
                collisions.append(other)
        return collisions


    """returns true if the given position is valid (a rectangle can potentially be placed there),
        returns false if the position is obstruceted"""
    def isValidPosition(self, pos: "Position") -> bool:
        for rect in self.rectangles:
            if rect.containsPoint(pos):
                return False
            
        return True
    
    def getRectWithPosition(self, pos : Position) -> Rectangle:
        for r in self.rectangles:
            if r.containsPoint(pos):
                return r
        return 
    
    def getDensity(self) -> float:
        """returns the density of the container (total rectangle area / total container area)"""
        totalRectVolume = 0
        for r in self.rectangles:
            totalRectVolume += r.width * r.height
        contArea = self.width * self.height
        return totalRectVolume / contArea