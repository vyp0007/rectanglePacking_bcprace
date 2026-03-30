from basicComponents.rectangle import Rectangle, Position
from basicComponents.rectangleContainer import Container
from utils import rectangleSortedList

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
         

def slideLeft(container : Container, rectangle : Rectangle, startPos : Position, placedRectsSorted : rectangleSortedList.RectangleSortedList):
    """attempts to slide the provided rectangle on provided position as far left as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(0, startPos.y)
    collisionCheckRect = Rectangle(startPos.x,rectangle.height,newPosition.x,newPosition.y)

    for r in placedRectsSorted.iter_right_desc():
        if r.overlaps(collisionCheckRect):
            newPosition = Position(r.x + r.width, newPosition.y)
            break


    if(newPosition.x >= startPos.x):
        return False
    return newPosition

def slideDown(container : Container, rectangle : Rectangle, startPos : Position, placedRectsSorted : rectangleSortedList.RectangleSortedList):
    """attempts to slide the provided rectangle on provided position as low as possible
        returns the new possition on success, return False on failure"""
    newPosition = Position(startPos.x, 0)
    collisionCheckRect = Rectangle(rectangle.width,startPos.y,newPosition.x,newPosition.y)

    for r in placedRectsSorted.iter_top_desc():
        if r.overlaps(collisionCheckRect):
            newPosition = Position(newPosition.x, r.y + r.height)
            break

    if(newPosition.y >= startPos.y):
        return False
    return newPosition


def placeRectangle(container : Container, rectangle : Rectangle, placedRectsSorted : rectangleSortedList.RectangleSortedList) -> Position:
    """places rectangle into the container by repeatedly moving it down and to the left as much as pussible
    DOES NOT ACTUALLY PUT THE RECTANGLE INTO CONTAINER, only returns the position for placement"""
    rectPos = Position(container.width - rectangle.width, container.height)
    slidDown = True
    slidLeft = True
    while slidDown or slidLeft:
        #print("moving rectangle")
        newPosition = slideDown(container,rectangle,rectPos,placedRectsSorted)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidDown = True
        else:
             slidDown = False
        newPosition = slideLeft(container,rectangle,rectPos,placedRectsSorted)
        if newPosition != False:
             rectPos.x = newPosition.x
             rectPos.y = newPosition.y
             slidLeft = True
        else:
             slidLeft = False  
    #print("place stoped")
    return rectPos



def bottom_left_fill(container_width, rectangles: list[Rectangle],optimised : bool = True) -> Container:
    cont = Container(container_width)
    placedRectsSorted = rectangleSortedList.RectangleSortedList()
    for rect in rectangles:
        #print("DEBUG width:", rect.width)
        rectPos = placeRectangle(cont,rect,placedRectsSorted)
        rect.setPosition(rectPos)
        cont.add_rectangle(rect)
        placedRectsSorted.add(rect)
        #print("rectangle placed")

    return cont