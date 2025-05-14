import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

def mandelbrote(c, maxIter):
    z = 0
    for i in range(maxIter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return maxIter

def mandelbrote_set(xmin, xmax, ymin, ymax, width, height, maxIter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)

    res = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            res[i, j] = mandelbrote(c, maxIter)
    return res


xmin, xmax, ymin, ymax, width, height = -2, 1, -1.5, 1.5, 1000, 1000
initial_resolution= 200
maxIter = 40
initial_max_iter = 40
result = mandelbrote_set(xmin, xmax, ymin, ymax, width, height, maxIter)

"""
plt.imshow(result, extent=[xmin, xmax, ymin, ymax], cmap='hot')
plt.colorbar()
plt.show()

"""


fig, ax = plt.subplots()
image = ax.imshow(result, extent=[xmin, xmax,
                                   ymin, ymax],
                  origin='lower', cmap='hot')
plt.colorbar(image)

prev_xlim = ax.get_xlim()
prev_ylim = ax.get_ylim()

initial_width = xmax - xmin
initial_height = ymax - ymin

def on_zoom(event):
    """Обработчик события изменения масштаба."""
    global prev_xlim, prev_ylim, initial_resolution, initial_max_iter
    
    if event.inaxes != ax:
        return
    
    new_xlim = ax.get_xlim()
    new_ylim = ax.get_ylim()
    
    if (new_xlim, new_ylim) == (prev_xlim, prev_ylim):
        return
    
    current_width = new_xlim[1] - new_xlim[0]
    current_height = new_ylim[1] - new_ylim[0]
    
    # Вычисление масштаба для адаптивного разрешения и итераций
    scale_factor_width = initial_width / current_width
    scale_factor_height = initial_height / current_height
    scale_factor = max(scale_factor_width, scale_factor_height)
    
    new_resolution = int(initial_resolution * scale_factor)
    new_max_iter = int(initial_max_iter * scale_factor)
    
    # Ограничения для предотвращения перегрузки
    new_resolution = min(new_resolution, 2000)
    new_max_iter = min(new_max_iter, 1000)
    
    # Пересчёт фрактала
    mandel = mandelbrote_set(new_xlim[0], new_xlim[1],
                        new_ylim[0], new_ylim[1],
                        new_resolution, new_resolution, new_max_iter)
    
    # Обновление изображения
    image.set_data(mandel)
    image.set_extent([new_xlim[0], new_xlim[1], new_ylim[0], new_ylim[1]])
    fig.canvas.draw_idle()
    
    prev_xlim, prev_ylim = new_xlim, new_ylim

# Привязка обработчика к событию отпускания кнопки мыши
fig.canvas.mpl_connect('button_release_event', on_zoom)

plt.show()
    
