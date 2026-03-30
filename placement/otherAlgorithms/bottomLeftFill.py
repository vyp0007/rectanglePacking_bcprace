from basicComponents.rectangle import Rectangle, Position
from basicComponents.rectangleContainer import Container
from sortedcontainers import SortedList


def getRightmostEdge(rects : list[Rectangle]):
    """returns the rightmost edge (float) from the provided list of rectangles"""
    if len(rects) == 0:
         return None
    retval = rects[0].x + rects[0].width
    for r in rects:
         if r.x + r.width >= retval:
              retval = r.x + r.width
    return retval

def getTopEdge(rects : list[Rectangle]):
    """returns the top edge (float) from the provided list of rectangles"""
    if len(rects) == 0:
         return None
    retval = rects[0].y + rects[0].height
    for r in rects:
         if r.y + r.height >= retval:
              retval = r.y + r.height
    return retval
         

def slideLeft(container : Container, rectangle : Rectangle, startPos : Position):
    """attempts to slide the provided rectangle on provided position as far left as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(0, startPos.y)
    collisionCheckRect = Rectangle(startPos.x,rectangle.height)

    if((not container.canPlaceRect(collisionCheckRect,newPosition))):
        newX = getRightmostEdge(container.getCollidingRectangles(collisionCheckRect, newPosition))
        if newX != None:
            newPosition.x = newX

    if(newPosition.x >= startPos.x):
        return False
    return newPosition

def slideLeft_bruteForce(container : Container, rectangle : Rectangle, startPos : Position):
    """attempts to slide the provided rectangle on provided position as far left as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(0, startPos.y)
    collisionCheckRect = Rectangle(startPos.x,rectangle.height)

    if((not container.canPlaceRect_old(collisionCheckRect,newPosition))):
        newX = getRightmostEdge(container.getCollidingRectangles_old(collisionCheckRect, newPosition))
        if newX != None:
            newPosition.x = newX

    if(newPosition.x >= startPos.x):
        return False
    return newPosition

def slideDown(container : Container, rectangle : Rectangle, startPos : Position):
    """attempts to slide the provided rectangle on provided position as low as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(startPos.x, 0)
    collisionCheckRect = Rectangle(rectangle.width,startPos.y)

    if((not container.canPlaceRect(collisionCheckRect,newPosition))):
       # print("adjusting up")
        newY = getTopEdge(container.getCollidingRectangles(collisionCheckRect, newPosition))
        if newY != None:
            newPosition.y = newY

    if(newPosition.y >= startPos.y):
        return False
    return newPosition

def slideDown_bruteForce(container : Container, rectangle : Rectangle, startPos : Position):
    """attempts to slide the provided rectangle on provided position as low as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(startPos.x, 0)
    collisionCheckRect = Rectangle(rectangle.width,startPos.y)

    if((not container.canPlaceRect_old(collisionCheckRect,newPosition))):
       # print("adjusting up")
        newY = getTopEdge(container.getCollidingRectangles_old(collisionCheckRect, newPosition))
        if newY != None:
            newPosition.y = newY

    if(newPosition.y >= startPos.y):
        return False
    return newPosition

def placeRectangle(container : Container, rectangle : Rectangle) -> Position:
    """places rectangle into the container by repeatedly moving it down and to the left as much as pussible"""
    rectPos = Position(container.width - rectangle.width, container.height)
    slidDown = True
    slidLeft = True
    while slidDown or slidLeft:
        #print("moving rectangle")
        newPosition = slideDown(container,rectangle,rectPos)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidDown = True
        else:
             slidDown = False
        newPosition = slideLeft(container,rectangle,rectPos)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidLeft = True
        else:
             slidLeft = False  
    #print("place stoped")
    return rectPos

def placeRectangle_bruteForce(container : Container, rectangle : Rectangle) -> Position:
    """places rectangle into the container by repeatedly moving it down and to the left as much as pussible"""
    rectPos = Position(container.width - rectangle.width, container.height)
    slidDown = True
    slidLeft = True

    while slidDown or slidLeft:
        newPosition = slideDown_bruteForce(container,rectangle,rectPos)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidDown = True
        else:
             slidDown = False
        newPosition = slideLeft_bruteForce(container,rectangle,rectPos)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidLeft = True
        else:
             slidLeft = False  

    return rectPos


def bottom_left_fill(container_width, rectangles: list[Rectangle],optimised : bool = True) -> Container:
    cont = Container(container_width)
    if optimised:
        for rect in rectangles:
            #print("DEBUG width:", rect.width)
            rectPos = placeRectangle(cont,rect)
            rect.setPosition(rectPos)
            cont.add_rectangle(rect)
            #print("rectangle placed")
    else:
        for rect in rectangles:
            rectPos = placeRectangle_bruteForce(cont,rect)
            rect.setPosition(rectPos)
            cont.add_rectangle(rect)

    return cont