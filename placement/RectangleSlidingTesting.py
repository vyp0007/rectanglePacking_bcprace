from basicComponents.rectangle import Rectangle
from basicComponents.dynamicContainer import DynamicContainer
from basicComponents.rectangle import Position


def overlaps_y(rect : Rectangle, y, h):
    return not (rect.y + rect.height <= y or y + h <= rect.y)

def overlaps_x(rect: Rectangle, x, w):
    return not (rect.x + rect.width <= x or x + w <= rect.x)

def slide_horizontal(rect : Rectangle, candidatePos : Position,container : DynamicContainer):
    """
    Adjust rect.x while keeping rect.y fixed.
    Returns Position or none
    """

    x_L = 0
    x_R = container.width

    placed_rectangles = container.rectangles

    for r in placed_rectangles:
        # filter rectangles taht cannot collide due to Y
        if not overlaps_y(r, candidatePos.y, rect.height):
            continue

        # Decide group (left/right)
        if r.x + r.width / 2 <= candidatePos.x + rect.width / 2:
            # adjust X_L
            x_L = max(x_L, r.x + r.width)
        else:
            # adjust X_R
            x_R = min(x_R, r.x - rect.width)

    # Check feasibility
    if x_L > x_R:
        return None

    #rect.x = x_L

    return Position(x_L,candidatePos.y)

def slide_vertical(rect: Rectangle, candidatePos: Position, container: DynamicContainer):
    """
    Adjust rect.y while keeping rect.x fixed.
    Returns Position or None.
    """

    y_B = 0
    y_A = container.height

    for r in container.rectangles:
        # Filter rectangles that cannot collide due to X
        if not overlaps_x(r, candidatePos.x, rect.width):
            continue

        # Decide group (bottom/top)
        if r.y + r.height / 2 <= candidatePos.y + rect.height / 2:
            # BELOW 
            y_B = max(y_B, r.y + r.height)
        else:
            # ABOVE 
            y_A = min(y_A, r.y - rect.height)

    # Check feasibility
    if y_B > y_A:
        return None

    return Position(candidatePos.x, y_B)

def evaluatePosition(rectangle : Rectangle, position : Position, container : DynamicContainer):
    """tests the fitness of placing the provided rectangle on provided position within provided dynamic container
    returns resulting width + height (lower value = better fitness)"""
    testRes = container.testRectanglePlacement(rectangle,position)
    return testRes[0] * testRes[1]

def findPostion(rect: Rectangle, container: DynamicContainer, positions : set[Position],direction: float) -> Position:
    """finds best position for placing the provided rectangle to the container"""

    best_pos = None
    best_score = float('inf')

    for p in positions:
        if direction < 0.5:
            pos1 = slide_horizontal(rect, p, container)
            if pos1 is None:
                continue

            pos2 = slide_vertical(rect, pos1, container)
            if pos2 is None:
                continue

        else:
            pos1 = slide_vertical(rect, p, container)
            if pos1 is None:
                continue

            pos2 = slide_horizontal(rect, pos1, container)
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

def addPositions(newRectangle: Rectangle, container: DynamicContainer, positions: set[Position]):

    x = newRectangle.x
    y = newRectangle.y
    w = newRectangle.width
    h = newRectangle.height
    
    positions.add(Position(newRectangle.x, newRectangle.y + newRectangle.height))
    positions.add(Position(newRectangle.x + newRectangle.width,newRectangle.y))
    positions.add(Position(newRectangle.x + newRectangle.width,newRectangle.y + newRectangle.height))


def posKilledByRect(pos : Position, rectangle : Rectangle):
    return (pos.x >= rectangle.x and pos.x < (rectangle.x + rectangle.width) and
            pos.y >= rectangle.y and pos.y < (rectangle.y + rectangle.height))

def cleanPositions(positions : set[Position], newRectangle : Rectangle):
    dead = set()
    for pos in positions:
        if posKilledByRect(pos,newRectangle):
            dead.add(pos)
            #print("position deleted")
    positions -= dead



def rectangle_sliding(rectangles: list[Rectangle], initialDirections : list[float]) -> DynamicContainer:
    positions = set()
    positions.add(Position(0,0))
    cont = DynamicContainer()
    for r, direction in zip(rectangles, initialDirections):
        rectPosition = findPostion(r,cont,positions,direction)
        if rectPosition is None:
            raise ValueError(f"Failed to place rectangle: {r}")
        r.setPosition(rectPosition)
        cont.add_rectangle(r)
        cleanPositions(positions, r)
        addPositions(r,cont,positions)

    
    return cont