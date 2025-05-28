import random
import matplotlib.pyplot as plt
import math


fig, ax = None, None
line = None
fill = None
current_terrain = []
START_X = 0

def midpointDisplacement(start, end, iterations, r):
    points = [start, end]
    
    for i in range(iterations):
        newPoints = []
        for j in range(len(points)-1):
            newP_x = (points[j][0] + points[j+1][0])/2
            newP_y = (points[j][1] + points[j+1][1])/2
            #h = len/(2^r)
            length = ((points[j][0] - points[j+1][0])**2 + (points[j][1] - points[j+1][1])**2)
            length = math.sqrt(length)/(2**r)
            newP = (newP_x, newP_y + random.uniform(-length, length))
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

def update_plot():
    global line, fill, ax, current_terrain
    x = [p[0] for p in current_terrain]
    y = [p[1] for p in current_terrain]
    min_y = min(y) if y else 0
    
    line.set_data(x, y)
    if fill:
        fill.remove()
    fill = ax.fill_between(x, y, min_y - 0.1, color='lightgreen', alpha=0.1)
    ax.figure.canvas.draw()

def handle_key(event):
    global current_terrain, ax
    x_min, x_max = ax.get_xlim()
    delta = (x_max - x_min) * 0.05
    
    if event.key == 'left':
        new_end = current_terrain[0]
        length = abs(new_end[0] - (new_end[0] - delta))
        new_start = (new_end[0] - delta, new_end[1] + random.uniform(-length, length))
        new_segment = midpointDisplacement(new_start, new_end, ITERATIONS, R)[:-1]
        current_terrain = new_segment + current_terrain
        ax.set_xlim(x_min - delta, x_max - delta)
        
    elif event.key == 'right':
        new_start = current_terrain[-1]
        length = abs(new_start[0] - (new_start[0] + delta))
        new_end = (new_start[0] + delta, new_start[1] + random.uniform(-length, length))
        new_segment = midpointDisplacement(new_start, new_end, ITERATIONS, R)[1:]
        current_terrain += new_segment
        ax.set_xlim(x_min + delta, x_max + delta)
    
    update_plot()


#random.uniform(-10, 10)
START = (0, random.uniform(-10, 10))
END = (50, random.uniform(-10, 10))
ITERATIONS = 10
R = 1.5

current_terrain = midpointDisplacement(START, END, ITERATIONS, R)
#plot_terrain(current_terrain)


fig, ax = plt.subplots(figsize=(12, 6))
line, = ax.plot([], [], 'g', linewidth=0.8)
ax.set_title("Midpoint Displacement")
fig.canvas.mpl_connect('key_press_event', handle_key)

update_plot()
ax.set_xlim(START[0], END[0])
plt.show()
