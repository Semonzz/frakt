import random
import matplotlib.pyplot as plt
import math


def midpointDisplacement(start, end, iterations, r):
    points = [start, end]
    
    for i in range(iterations):
        newPoints = []
        for j in range(len(points)-1):
            newP_x = (points[j][0] + points[j+1][0])/2
            newP_y = (points[j][1] + points[j+1][1])/2
            #h = len/(2^r)
            lenght = ((points[j][0] - points[j+1][0])**2 + (points[j][1] - points[j+1][1])**2)
            lenght = math.sqrt(lenght)/(2**r)
            newP = (newP_x, newP_y + random.uniform(-lenght, lenght))
            newPoints.append(points[j])
            newPoints.append(newP)
        newPoints.append(points[-1])
        points = newPoints;
    return points

   
def plot_terrain(points):
    plt.figure(figsize=(12, 6))
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    plt.plot(x, y, 'g', linewidth=0.8)
    plt.fill_between(x, y, min(y) - 0.1, color='lightgreen', alpha=0.1)
    plt.title("Midpoint Displacement")
    plt.show()

#random.uniform(-10, 10)
START = (0, random.uniform(-10, 10))
END = (50, random.uniform(-10, 10))
ITERATIONS = 5
R = 1.5

terrain = midpointDisplacement(START, END, ITERATIONS, R)
plot_terrain(terrain)


