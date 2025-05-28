import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import random

def diamond_square(size, R):
    heightMap = np.zeros((size, size))

    heightMap[0][0] = random.uniform(-1, 1)
    heightMap[size-1][0] = random.uniform(-1, 1)
    heightMap[0][size-1] = random.uniform(-1, 1)
    heightMap[size-1][size-1] = random.uniform(-1, 1)

    chunk_size = size - 1
    iteration = 0

    while chunk_size > 1:
        iteration += 1
        step = chunk_size // 2

        # Square
        for y in range(0, size - 1, chunk_size):
            for x in range(0, size - 1, chunk_size):
                avg = (heightMap[y][x] + heightMap[y + chunk_size][x] +
                       heightMap[y][x + chunk_size] + 
                       heightMap[y + chunk_size][x + chunk_size]) / 4
                noise = random.uniform(-1, 1) * (R ** iteration)
                heightMap[y + step][x + step] = avg + noise

        # Diamond
        for y in range(0, size, step):
            for x in range((y + step) % (2 * step), size, 2 * step):
                summ = 0
                cnt = 0
                if x - step >= 0:
                    cnt += 1
                    summ+=heightMap[y][x - step]
                if x + step < size:
                    cnt += 1
                    summ+=heightMap[y][x + step]
                if y - step >= 0:
                    cnt += 1
                    summ+=heightMap[y - step][x]
                if y + step < size:
                    cnt += 1
                    summ+=heightMap[y + step][x]
                if summ!=0:
                    noise = random.uniform(-1, 1) * (R ** iteration)
                    heightMap[y][x] = (summ / cnt) + noise
                else:
                    noise = random.uniform(-1, 1) * (R ** iteration)
                    heightMap[y][x] = noise

        chunk_size = step

    return heightMap

def plot_heightmap(heightmap, cmap='terrain'):
    plt.figure(figsize=(9, 7))
    plt.imshow(heightmap, cmap=cmap, origin='lower')
    plt.colorbar(label='Height')
    plt.title("Diamond-Square Heightmap")
    plt.axis('off')
    plt.show()

MAP_SIZE = 257
R = 0.7

heightmap = diamond_square(MAP_SIZE, R)
plot_heightmap(heightmap)
