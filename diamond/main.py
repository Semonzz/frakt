import numpy as np
import matplotlib.pyplot as plt
import random


def diamond_square(size, R, const):
    heightMap = np.zeros((size, size))
    
    heightMap[0][0] = -100
    heightMap[size-1][0] = -80
    heightMap[0][size-1] = 100
    heightMap[size-1][size-1] = 20

    chunckSize = size - 1
    iteration = 0
    while chunckSize > 1:
        iteration += 1
        step = chunckSize // 2

        #square
        for y in range(0, size-1, chunckSize):
            for x in range(0, size-1, chunckSize):
                heightMap[y + step][x + step] = (
                    heightMap[y][x] + heightMap[y + chunckSize][x] +
                    heightMap[y][x + chunckSize] +
                    heightMap[y + chunckSize][x + chunckSize])/4 + random.uniform(-(R**iteration), (R**iteration))
        
        #diamond
        for y in range(0, size-1, step):
            for x in range((y + step) % chunckSize, size - 1, chunckSize):
                cnt = 4
                if (y - step < 0): cnt -= 1
                if (y + step > size): cnt -= 1
                if (x - step < 0): cnt -= 1
                if (x + step > size): cnt -= 1
                heightMap[y][x] = (
                    heightMap[y][x - step] + heightMap[y - step][x] +
                    heightMap[y + step][x] + heightMap[y][x + step])/cnt + random.uniform(-(R**iteration), (R**iteration))
                
        
        chunckSize //= 2
    return heightMap


def plot_heightmap(heightmap, cmap='terrain'):
    plt.figure(figsize=(9, 7))
    plt.imshow(heightmap, cmap=cmap, origin='lower')
    plt.colorbar(label='Высота')
    plt.title("Diamond-Square Heightmap")
    plt.axis('off')
    plt.show()


MAP_SIZE = 513
R = 1.2
CONST = 2

heightmap = diamond_square(MAP_SIZE, R, CONST)
#print(heightmap)
plot_heightmap(heightmap)
