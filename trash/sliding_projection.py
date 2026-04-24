
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