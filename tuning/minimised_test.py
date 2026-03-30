
import time

from utils.rectangleFileLoader import load_rectangles_from_json
from geneticAlgorithms.simannealSA import SimulatedAnnealing


config = {"Tmax":100,"Tmin":0.01,"steps":3000}
dataset = load_rectangles_from_json("problems/small_125.json")

startTime = time.time()

for i in range(0,5):
    sa = SimulatedAnnealing(dataset[1],dataset[0],config)
    iterStart = time.time()
    res = sa.run()
    iterend = time.time()
    print("iter ", i, " time: ",iterend - iterStart, "fitness: ",res["fitness"])




endtime = time.time()
print("TOTAL RUNTIME: ",endtime - startTime)