
import json

from basicComponents.rectangle import Rectangle


def load_rectangles_from_json(filename: str, sumVolume = True, printOutput = True) -> tuple[int, list[Rectangle]]:
    with open(filename, "r") as f:
        data = json.load(f)

    width = data["Width"]
    rects = [Rectangle(r["width"], r["height"]) for r in data["Rectangles"]]
    sum = 0
    if sumVolume:        
        for r in rects:
            sum += r.width * r.height
            if r.width <= 0 or r.height <= 0:
                print("FLAT RECTANGLE!")

    if printOutput:
        print("Loaded rectangles: ", len(rects) , "\nContainer width: ",width)
    if(sumVolume):
        print("Volume: ",sum)

    return width, rects