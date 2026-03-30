from basicComponents.rectangle import Rectangle, Position
from basicComponents.rectangleContainer import Container
from sortedcontainers import SortedList


class AdjustablePosition(Position):
    def __init__(self, x, y, destination : float, vertical : bool):
        super().__init__(x, y)
        self.destination = destination
        #is true if this is meant to move along the x axis
        self.vertical = vertical
        if(vertical):
            if(self.y > self.destination):
                raise ValueError("destination cannot be < y for vertical AdjustablePosition")
        else:
            if(self.x > self.destination):
                raise ValueError("destination cannot be < x for vertical AdjustablePosition")
        
    
    """returns true if destination was exceeded (this position was adjusted to its limits)"""
    def destinationExceeded(self) -> bool:
        if(self.vertical):
            if(self.y > self.destination):
                return True
        else:
            if(self.x > self.destination):
                return True
        return False
        
    def adjustPosition(self, cont : Container) -> bool:
        """
        adjusts own position so it is valid within the given container, returns true if a valid position was found
        returns false if destination was reached without discovering a valid position
        """
        i = 0
        rect = cont.getRectWithPosition(self)
        while(rect is not None):
            if(self.vertical):
                self.y = rect.y + rect.height                
            else:
                self.x = rect.x + rect.width
            if(self.destinationExceeded()):
                return False
            rect = cont.getRectWithPosition(self)
            #print(str(self) + " iteration " + str(i))
            i += 1
        return True
    
    def adjustForRectangle(self, cont : Container, rect : Rectangle):
        """
        adjusts own position so it is valid within the given container, assuming the only obstacle can be the provided rectangle, returns true if a valid position was found
        returns false if destination was reached without discovering a valid position
        """
        #TODO
        pass

            

def positionKey(pos : Position):
    return(pos.x,pos.y,pos._id)

#returns true if a rectangle can be moved between positions in "L" shape
def canSlide(rect : Rectangle, fromPos : Position, toPos : Position, cont : Container):
    
    if(cont.canPlaceRect(Rectangle(fromPos.x - toPos.x, rect.height),Position(toPos.x,fromPos.y)) and 
       cont.canPlaceRect(Rectangle(rect.width,fromPos.y - toPos.y),toPos)):
        return True
    
    if(cont.canPlaceRect(Rectangle(rect.width,fromPos.y - toPos.y),Position(fromPos.x,toPos.y)) and
       cont.canPlaceRect(Rectangle(fromPos.x - toPos.x,rect.height),toPos)):
        return True
    
    return False

def canSlideOld(rect : Rectangle, fromPos : Position, toPos : Position, cont : Container):
    
    if(cont.canPlaceRect_old(Rectangle(fromPos.x - toPos.x, rect.height),Position(toPos.x,fromPos.y)) and 
       cont.canPlaceRect_old(Rectangle(rect.width,fromPos.y - toPos.y),toPos)):
        return True
    
    if(cont.canPlaceRect_old(Rectangle(rect.width,fromPos.y - toPos.y),Position(fromPos.x,toPos.y)) and
       cont.canPlaceRect_old(Rectangle(fromPos.x - toPos.x,rect.height),toPos)):
        return True
    
    return False

def placeRectangle(cont : Container, rect : Rectangle, positions : SortedList, optimised) -> Position:
    """attempts to place the rectangle into the given container according to BLF
        returns the final position of the rectangle.
        Does NOT update the rectangles's own coordinates"""
    rectPos = Position(cont.width - rect.width, cont.height)
    for pos in reversed(positions):
        if pos.x <= rectPos.x:
            if pos.y <= rectPos.y:
                if optimised:
                    if canSlide(rect,rectPos,pos,cont):
                        rectPos = pos
                else:
                    if canSlideOld(rect,rectPos,pos,cont):
                        rectPos = pos
    
    return rectPos


def addPositionsByRectangle(rect : Rectangle, positions : SortedList, cont : Container):
    """adds positions to the provided list based on the newly added rectangles
(top left corner, bottom right corner, lowest available y from bottom right, lowest available x from top left)"""
    topLeft = Position(rect.x, rect.y + rect.height)
    
    lowestX = AdjustablePosition(0, rect.y + rect.height, topLeft.x, False)
    
    positions.add(topLeft) #top left corner
    valid = lowestX.adjustPosition(cont)
    if(valid):
        positions.add(lowestX)
    
    if(rect.x + rect.width < cont.width):
        bottomRight = Position(rect.x + rect.width, rect.y)
        positions.add(bottomRight)
        lowestY = AdjustablePosition(rect.x + rect.width, 0, bottomRight.y, True)
        valid = lowestY.adjustPosition(cont)
        if(valid):
            positions.add(lowestY)


def updatePositions(positions : SortedList, cont : Container, newRect : Rectangle):
    """
    removes invalid positions from provided list, updates adjustable positions
    """
    toUpdate = []
    toRemove = []
    for pos in positions:
        if(newRect.containsPoint(pos)):
            if(type(pos) is AdjustablePosition):
                toUpdate.append(pos)
            else:
                toRemove.append(pos)


    for r in toUpdate:
        positions.remove(r)
        valid = r.adjustPosition(cont)
        if(valid):
            positions.add(r)

    for r in toRemove:
        positions.remove(r)

    


def bottom_left_fill(container_width, rectangles: list[Rectangle],optimised : bool = False) -> Container:
    positions : SortedList = SortedList(key = positionKey)
    positions.add(Position(0,0))
    cont = Container(container_width)
    for rect in rectangles:
        #place rectangle
        pos = placeRectangle(cont,rect,positions,optimised)
        rect.setPosition(pos)
        #add rect to container
        cont.add_rectangle(rect)
        #add new positions
        addPositionsByRectangle(rect, positions, cont)
        #update positions
        updatePositions(positions,cont,rect)
        
        
    return cont