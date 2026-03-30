import sys
import random
from rectangle import Rectangle
import json
def main(width: int, cuts: int, levels: int, file):
    container = Rectangle(width, width)

    final_rects = split_rectangle(container, cuts, levels)

    save_rectangles_to_json(final_rects, width, file)


def split_rectangle(rect: Rectangle, cuts: int, levels: int) -> list[Rectangle]:

    if levels <= 0:
        return [rect]

    sub_rects = perform_cuts(rect, cuts)

    result = []
    for r in sub_rects:
        result.extend(split_rectangle(r, cuts, levels - 1))

    return result

def perform_cuts(rect: Rectangle, cuts: int) -> list[Rectangle]:

    width = rect.width
    height = rect.height

    workPosition = [0, 0]
    rects: list[Rectangle] = []

    #ensure cutting up of "noodles"
    if width > height:
        # vertical cut
            remaining_width = width - workPosition[0]
            cut = balancedRandomCut(remaining_width, cuts)

            new_rect = Rectangle(cut, height - workPosition[1])
            workPosition[0] += cut
            cuts -= 1
            rects.append(new_rect)
    elif height > width:
        # horizontal cut
            remaining_height = height - workPosition[1]
            cut = balancedRandomCut(remaining_height, cuts)

            new_rect = Rectangle(width - workPosition[0], cut)
            workPosition[1] += cut
            cuts -= 1
            rects.append(new_rect)

    for i in range(cuts):
        remaining_cuts = cuts - i

        
        if random.random() > 0.5:
            # vertical cut
            remaining_width = width - workPosition[0]

            if remaining_width <= 0:
                break

            cut = balancedRandomCut(remaining_width, remaining_cuts)

            new_rect = Rectangle(cut, height - workPosition[1])
            workPosition[0] += cut

        else:
            # horizontal cut
            remaining_height = height - workPosition[1]

            if remaining_height <= 0:
                break

            cut = balancedRandomCut(remaining_height, remaining_cuts)

            new_rect = Rectangle(width - workPosition[0], cut)
            workPosition[1] += cut

        rects.append(new_rect)

    # Remaining piece
    remaining_width = width - workPosition[0]
    remaining_height = height - workPosition[1]

    if remaining_width > 0 and remaining_height > 0:
        rects.append(Rectangle(remaining_width, remaining_height))

    return rects


def randomCut(number, minPart = 0.20, maxPart = 0.80):
    if(minPart > maxPart):
        raise ValueError("minPart is greater than maxPart")
    
    min_val = number * minPart
    max_val = number * maxPart
    random_value = random.uniform(min_val, max_val)
    #print("made a cut at " + str(random_value) + " with min " + str(minPart) + " max " + str(maxPart))
    return random_value

def balancedRandomCut(total_remaining: float, remaining_cuts: int, 
                      variation: float = 0.20):
    """
    Creates a cut close to equal partitioning but with randomness.
    variation = 0.25 means 25% deviation from equal size.
    """

    if remaining_cuts <= 1:
        return total_remaining

    equal_cut = total_remaining / remaining_cuts

    factor = random.uniform(1 - variation, 1 + variation)
    cut = equal_cut * factor

    min_remaining_needed = (remaining_cuts - 1) * (equal_cut * (1 - variation))
    max_allowed = total_remaining - min_remaining_needed

    return min(cut, max_allowed)


def save_rectangles_to_json(rects: list[Rectangle], containerWidth: int, filename: str):
    data = {
        "Width": containerWidth,
        "Rectangles": [
            {"width": rect.width, "height": rect.height} for rect in rects
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    try:
        num1 = int(sys.argv[1])  # width
        num2 = int(sys.argv[2])  # cuts
        num3 = int(sys.argv[3])  # levels
        filePath = sys.argv[4]

        main(num1, num2, num3, filePath)

    except ValueError:
        print("ERROR: first three parameters must be valid numbers")
    except IndexError:
        print("ERROR: usage <width> <cuts> <levels> <export file>")

