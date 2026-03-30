from utils.uniqueOrderedList import UniqueOrderedList
from rectangle import *
from rectangleContainer import *


def getBottomLeftPos(rect : Rectangle, container : Container, positionsX, positionsY) -> tuple[int,int]:
    #every available Y
    for posY in positionsY:
            rect.y = posY
            #every available x
            for posX in positionsX:
                rect.x = posX
                #if rect would exceed container
                if rect.x + rect.width > container.width:
                    #print(str(rect) + " doesnt fit")
                    break
                #check if rect fits
                if container.canPlaceRect_old(rect,Position(rect.x,rect.y)):
                    return (rect.x,rect.y)
                #else:
                 #   print(str(rect) + " overlaps")
    return None

def bottom_left_fill(container_width, rectangles: list[Rectangle]) -> Container:
    """
    Packs rectangles using the bottom-left algorithm.
    Returns a NEW list of rectangles with computed positions (x, y).
    The input list is left unchanged.
    """
    #placed = []
    cont = Container(container_width)
    positionsX = UniqueOrderedList()
    positionsX.add(0)
    positionsY = UniqueOrderedList()
    positionsY.add(0)

    for original_rect in rectangles:
        # Create a NEW rectangle instance (same width/height, fresh color)
        rect = Rectangle(original_rect.width, original_rect.height)
        rect.color = original_rect.color

        pos = getBottomLeftPos(rect, cont, positionsX, positionsY)
        if pos is None:
            print("PACKING IMPOSSIBLE")
            return []

        rect.x, rect.y = pos
        positionsX.add(rect.x + rect.width)
        positionsY.add(rect.y + rect.height)
        #placed.append(rect)
        cont.add_rectangle(rect)

    return cont




"""
def sortPositionsByY(positions : List[Position]):
    positions.sort(key=lambda pos: pos.y)

def initialPlacement(container : Container, rect: Rectangle, positions : List[Position]):
    #rectPos = Position(container.width - rect.width,container.height)
    rect.x = container.width - rect.width
    rect.y = container.height
    for posCandidate in positions:
        if (container.canPlaceRect(Rectangle(rect.width,rect.y - posCandidate.y),Position(rect.x,posCandidate.y))
            and container.canPlaceRect(Rectangle(rect.x - posCandidate.x,rect.height),Position(posCandidate.x,rect.y))):
                #CAN BE REACHED BY SLIDING DOWN AND LEFT
                rect.x = posCandidate.x
                rect.y = posCandidate.y
                return True
        
    return False


def removePositionFromList(positions: List[Position], position_to_remove: Position):
    try:        
        positions.remove(position_to_remove)
        return True
    except ValueError:        
        return False

def bottomLeftFill(container : Container, rectangles : list[Rectangle]):
    positions: List[Position] = []
    positions.append(Position(0,0))
    for rect in rectangles:
        sortPositionsByY(positions)
        #INITIALLY PLACE RECT
        initialPlacement(container,rect,positions)        
        #WHILE POSSIBLE SLIDE RECT
        #TODO
        #DELETE POSITION
        removePositionFromList(positions,Position(rect.x,rect.y))
        #ADD RECT TO CONTAINER
        if container.canPlaceRect(rect,Position(rect.x,rect.y)):
            container.add_rectangle(rect)
        else:
             print("STUPID DUMBASS ERROR")
        #ADD POSITIONS
        positions.append(Position(rect.x,rect.y + rect.height + 1))
        positions.append(Position(rect.x + rect.width + 1, rect.y))
        #TODO
"""
