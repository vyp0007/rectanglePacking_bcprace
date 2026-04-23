from basicComponents.rectangle import Rectangle
from basicComponents.dynamicContainer import DynamicContainer
from basicComponents.rectangle import Position
from placement.placement_utils.SortedListsForSliding import RectangleSortedList

def overlaps_y(rect : Rectangle, y, h):
    return not (rect.y + rect.height <= y or y + h <= rect.y)

def overlaps_x(rect: Rectangle, x, w):
    return not (rect.x + rect.width <= x or x + w <= rect.x)

def slide_horizontal(rect : Rectangle, candidatePos : Position,container : DynamicContainer, placedRects : RectangleSortedList):
    """
    Adjust rect.x while keeping rect.y fixed.
    Returns Position or none
    """

    x_L = 0
    x_R = container.width


    # FIND MAX LEFT
    for r in placedRects.iter_right_desc():
        #filter rectangles taht cannot collide due to Y
        if not overlaps_y(r, candidatePos.y, rect.height):
            continue

        #decide group left/right
        if r.x + r.width / 2 <= candidatePos.x + rect.width / 2:
            # LEFT
            x_L = r.x + r.width
            break
        

    for r in placedRects.by_left:
        #filter rectangles taht cannot collide due to Y
        if not overlaps_y(r, candidatePos.y, rect.height):
            continue

        #decide group left/right
        if r.x + r.width / 2 <= candidatePos.x + rect.width / 2:
           continue
        else:
            # RIGHT
            x_R = r.x - rect.width
            break

    # Check feasibility
    if x_L > x_R:
        return None

    #rect.x = x_L

    return Position(x_L,candidatePos.y)

def slide_vertical(rect: Rectangle, candidatePos: Position, container: DynamicContainer, placedRects : RectangleSortedList):
    """
    Adjust rect.y while keeping rect.x fixed.
    Returns Position or None.
    """

    y_B = 0
    y_A = container.height

    #FIND MAX BELOW
    for r in placedRects.iter_top_desc():
        #filter rectangles that cannot collide due to X
        if not overlaps_x(r, candidatePos.x, rect.width):
            continue

        #decide group bottom/top
        if r.y + r.height / 2 <= candidatePos.y + rect.height / 2:
            # BELOW 
            y_B = r.y + r.height
            break
        
    #FIND MIN ABOVE
    for r in placedRects.by_bottom:
        #filter rectangles that cannot collide due to X
        if not overlaps_x(r, candidatePos.x, rect.width):
            continue

        #decide group bottom/top
        if r.y + r.height / 2 <= candidatePos.y + rect.height / 2:
            continue
        else:
            # ABOVE 
            y_A = r.y - rect.height
            break

    #check feasibility
    if y_B > y_A:
        return None

    return Position(candidatePos.x, y_B)

def evaluatePosition(rectangle : Rectangle, position : Position, container : DynamicContainer):
    """tests the fitness of placing the provided rectangle on provided position within provided dynamic container
    returns resulting width + height (lower value = better fitness)"""
    testRes = container.testRectanglePlacement(rectangle,position)
    return testRes[0] * testRes[1]

def findPostion(rect: Rectangle, container: DynamicContainer, positions : set[Position],direction: float, placedRects : RectangleSortedList) -> Position:
    """finds best position for placing the provided rectangle to the container"""

    best_pos = None
    best_score = float('inf')

    for p in positions:
        if direction < 0.5:
            pos1 = slide_horizontal(rect, p, container, placedRects)
            if pos1 is None:
                continue

            pos2 = slide_vertical(rect, pos1, container, placedRects)
            if pos2 is None:
                continue

        else:
            pos1 = slide_vertical(rect, p, container, placedRects)
            if pos1 is None:
                continue

            pos2 = slide_horizontal(rect, pos1, container, placedRects)
            if pos2 is None:
                continue

        score = evaluatePosition(rect, pos2, container)

        if score < best_score:
            best_score = score
            best_pos = pos2
        #EVALUATING INTERMEDIATE POSITION
        """
        score1 = evaluatePosition(rect, pos1, container)
        if score1 < best_score:
            best_score = score1
            best_pos = pos1
        """

    return best_pos

def project_horizontal(x: float, y: float, container: DynamicContainer) -> Position | None:
    """Project horizontally from (x, y) to nearest obstacle"""

    best_dist = float('inf')
    best_x = None

    for r in container.rectangles:
        # must intersect horizontal line
        if r.y <= y <= r.y + r.height:

            # left
            if r.x + r.width <= x:
                dist = x - (r.x + r.width)
                if dist < best_dist:
                    best_dist = dist
                    best_x = r.x + r.width

            # right
            elif r.x >= x:
                dist = r.x - x
                if dist < best_dist:
                    best_dist = dist
                    best_x = r.x

    if best_x is None:
        return None

    return Position(best_x, y)

def project_vertical(x: float, y: float, container: DynamicContainer) -> Position | None:
    """Project vertically from (x, y) to nearest obstacle"""

    best_dist = float('inf')
    best_y = None

    for r in container.rectangles:
        # must intersect vertical line
        if r.x <= x <= r.x + r.width:

            # below
            if r.y + r.height <= y:
                dist = y - (r.y + r.height)
                if dist < best_dist:
                    best_dist = dist
                    best_y = r.y + r.height

            # above
            elif r.y >= y:
                dist = r.y - y
                if dist < best_dist:
                    best_dist = dist
                    best_y = r.y

    if best_y is None:
        return None

    return Position(x, best_y)

def addPositions(newRectangle: Rectangle, container: DynamicContainer, positions: set[Position]):

    x = newRectangle.x
    y = newRectangle.y
    w = newRectangle.width
    h = newRectangle.height

    positions.add(Position(newRectangle.x, newRectangle.y + newRectangle.height))
    positions.add(Position(newRectangle.x + newRectangle.width,newRectangle.y))
    positions.add(Position(newRectangle.x + newRectangle.width,newRectangle.y + newRectangle.height))

    #vertically projected point
    """
    v_proj = project_vertical(x + w, y, container)
    if v_proj is not None:
        positions.add(v_proj)

    #horizontaly projected point
    h_proj = project_horizontal(x, y + h, container)
    if h_proj is not None:
        positions.add(h_proj)
    """


def rectangle_sliding(rectangles: list[Rectangle], initialDirections : list[float]) -> DynamicContainer:
    positions = set()
    positions.add(Position(0,0))
    cont = DynamicContainer()
    placedSorted = RectangleSortedList()
    for r, direction in zip(rectangles, initialDirections):
        rectPosition = findPostion(r,cont,positions,direction,placedSorted)
        if rectPosition is None:
            raise ValueError(f"Failed to place rectangle: {r}")
        r.setPosition(rectPosition)
        cont.add_rectangle(r)
        addPositions(r,cont,positions)
        placedSorted.add(r)

    
    return cont