import numpy as np
import matplotlib.pyplot as plt
from numba import jit

pmin, pmax, qmin, qmax = -2.5, 1.5, -2, 2
ppoints, qpoints = 800, 600  #Разрешение экрана
max_iterations = 100
infinity_border = 10

@jit(nopython=True)
def mandelbrot(pmin, pmax, ppoints, qmin, qmax, qpoints, max_iterations=200, infinity_border=10):
    image = np.zeros((ppoints, qpoints))
    p = np.linspace(pmin, pmax, ppoints)
    q = np.linspace(qmin, qmax, qpoints)

    for i in range(ppoints):
        for j in range(qpoints):
            c = complex(p[i], q[j])
            z = 0
            n = 0
            while abs(z) <= infinity_border and n < max_iterations:
                z = z * z + c
                n += 1
            image[i, j] = n

    return image.T

def update_image():
    image = mandelbrot(pmin, pmax, ppoints, qmin, qmax, qpoints)
    plt.imshow(image, cmap='twilight_shifted', extent=(pmin, pmax, qmin, qmax), interpolation='bilinear')
    plt.axis('off')
    plt.draw()

plt.switch_backend('TkAgg')

plt.ion()
fig, ax = plt.subplots()
update_image()

def on_key(event):
    global pmin, pmax, qmin, qmax
    delta_x = (pmax - pmin) * 0.2  #Шаг перемещения по X
    delta_y = (qmax - qmin) * 0.2  #Шаг перемещения по Y

    if event.key == 'up':  #Вверх
        qmin -= delta_y
        qmax -= delta_y
    elif event.key == 'down':  #Вниз
        qmin += delta_y
        qmax += delta_y
    elif event.key == 'left':  #Влево
        pmin -= delta_x
        pmax -= delta_x
    elif event.key == 'right':  #Вправо
        pmin += delta_x
        pmax += delta_x

    update_image()

def on_click(event):
    global pmin, pmax, qmin, qmax
    scale_factor = 0.5

    center_x = (pmin + pmax) / 2
    center_y = (qmin + qmax) / 2

    if event.button == 1:
        delta_x = (pmax - pmin) * scale_factor
        delta_y = (qmax - qmin) * scale_factor
        pmin = center_x - delta_x / 2
        pmax = center_x + delta_x / 2
        qmin = center_y - delta_y / 2
        qmax = center_y + delta_y / 2
    elif event.button == 3:
        delta_x = (pmax - pmin) * (scale_factor * 4)
        delta_y = (qmax - qmin) * (scale_factor * 4)
        pmin = center_x - delta_x / 2
        pmax = center_x + delta_x / 2
        qmin = center_y - delta_y / 2
        qmax = center_y + delta_y / 2

    min_zoom = 1e-5
    if (pmax - pmin) < min_zoom or (qmax - qmin) < min_zoom:
        return

    update_image()

fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show(block=True)
