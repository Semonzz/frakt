import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import matplotlib.colors as colors


class MandelbrotFractal:
    def __init__(self):
        self.z0 = complex(0, 0)
        self.N = 150
        self.R = 2.0
        self.a = 1.5
        self.width, self.height = 600, 600
        self.colormap = 'twilight_shifted'
        
        self.x_min, self.x_max = -self.a, self.a
        self.y_min, self.y_max = -self.a, self.a

        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        plt.subplots_adjust(bottom=0.4)

        self.create_controls()

        self.update_fractal()

    def create_controls(self):
        #sliders
        ax_re_z0 = plt.axes([0.25, 0.35, 0.65, 0.03])
        self.slider_re_z0 = Slider(ax_re_z0, 'Re(z0)', -2.0, 2.0, valinit=self.z0.real)

        ax_im_z0 = plt.axes([0.25, 0.30, 0.65, 0.03])
        self.slider_im_z0 = Slider(ax_im_z0, 'Im(z0)', -2.0, 2.0, valinit=self.z0.imag)

        ax_a = plt.axes([0.25, 0.25, 0.65, 0.03])
        self.slider_a = Slider(ax_a, 'a (area)', 0.1, 5.0, valinit=self.a)

        ax_N = plt.axes([0.25, 0.20, 0.65, 0.03])
        self.slider_N = Slider(ax_N, 'N (iterations)', 20, 500, valinit=self.N, valstep=10)

        ax_R = plt.axes([0.25, 0.15, 0.65, 0.03])
        self.slider_R = Slider(ax_R, 'R (radius)', 0.5, 5.0, valinit=self.R)

        #buttons
        ax_zoom_in = plt.axes([0.15, 0.05, 0.1, 0.05])
        ax_zoom_out = plt.axes([0.27, 0.05, 0.1, 0.05])
        ax_move_left = plt.axes([0.39, 0.05, 0.1, 0.05])
        ax_move_right = plt.axes([0.51, 0.05, 0.1, 0.05])
        ax_move_up = plt.axes([0.63, 0.05, 0.1, 0.05])
        ax_move_down = plt.axes([0.75, 0.05, 0.1, 0.05])
        ax_reset = plt.axes([0.87, 0.05, 0.1, 0.05])

        self.btn_zoom_in = Button(ax_zoom_in, 'Increase (x2)')
        self.btn_zoom_out = Button(ax_zoom_out, 'Decrease (x2)')
        self.btn_move_left = Button(ax_move_left, '← 10%')
        self.btn_move_right = Button(ax_move_right, '→ 10%')
        self.btn_move_up = Button(ax_move_up, '↑ 10%')
        self.btn_move_down = Button(ax_move_down, '↓ 10%')
        self.btn_reset = Button(ax_reset, 'Reset')

        self.slider_re_z0.on_changed(self.update_parameters)
        self.slider_im_z0.on_changed(self.update_parameters)
        self.slider_a.on_changed(self.update_a)
        self.slider_N.on_changed(self.update_parameters)
        self.slider_R.on_changed(self.update_parameters)

        self.btn_zoom_in.on_clicked(self.zoom_in)
        self.btn_zoom_out.on_clicked(self.zoom_out)
        self.btn_move_left.on_clicked(self.move_left)
        self.btn_move_right.on_clicked(self.move_right)
        self.btn_move_up.on_clicked(self.move_up)
        self.btn_move_down.on_clicked(self.move_down)
        self.btn_reset.on_clicked(self.reset_view)

    def update_parameters(self, val):
        self.z0 = complex(self.slider_re_z0.val, self.slider_im_z0.val)
        self.N = int(self.slider_N.val)
        self.R = self.slider_R.val
        self.update_fractal()

    def update_a(self, val):
        self.a = self.slider_a.val
        self.x_min, self.x_max = -self.a, self.a
        self.y_min, self.y_max = -self.a, self.a
        self.update_fractal()

    def mandelbrot_set(self):
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        c = x + 1j * y[:, None]
        
        z = np.full(c.shape, self.z0, dtype=np.complex128)
        iterations = np.full(c.shape, -1, dtype=np.int32)
        
        mask = np.abs(z) >= self.R
        iterations[mask] = 0
        
        active = ~mask
        
        for i in range(1, self.N + 1):
            z[active] = z[active] ** 2 + c[active]
            
            new_mask = (np.abs(z) >= self.R) & active
            iterations[new_mask] = i
            active &= ~new_mask

        return iterations

    def update_fractal(self):
        iterations = self.mandelbrot_set()

        cmap = plt.get_cmap(self.colormap)
        cmap.set_under('black')
        
        norm = colors.Normalize(vmin=0, vmax=self.N)
        
        self.ax.clear()
        self.ax.imshow(iterations, cmap=cmap, norm=norm,
                       extent=[self.x_min, self.x_max, self.y_min, self.y_max],
                       origin='lower')
        
        title = f'Mandelbrot set: zₙ₊₁ = zₙ² + c, z0 = {self.z0.real:.3f} + {self.z0.imag:.3f}i'
        self.ax.set_title(title)
        self.fig.canvas.draw_idle()

    def zoom_in(self, event):
        x_center = (self.x_min + self.x_max) / 2
        y_center = (self.y_min + self.y_max) / 2
        x_half = (self.x_max - self.x_min) / 4
        y_half = (self.y_max - self.y_min) / 4

        self.x_min = x_center - x_half
        self.x_max = x_center + x_half
        self.y_min = y_center - y_half
        self.y_max = y_center + y_half

        self.update_fractal()

    def zoom_out(self, event):
        x_center = (self.x_min + self.x_max) / 2
        y_center = (self.y_min + self.y_max) / 2
        x_half = (self.x_max - self.x_min)
        y_half = (self.y_max - self.y_min)

        self.x_min = x_center - x_half
        self.x_max = x_center + x_half
        self.y_min = y_center - y_half
        self.y_max = y_center + y_half

        self.update_fractal()

    def move_view(self, dx, dy):
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min

        self.x_min += dx * x_range
        self.x_max += dx * x_range
        self.y_min += dy * y_range
        self.y_max += dy * y_range

        self.update_fractal()

    def move_left(self, event):
        self.move_view(-0.1, 0)

    def move_right(self, event):
        self.move_view(0.1, 0)

    def move_up(self, event):
        self.move_view(0, 0.1)

    def move_down(self, event):
        self.move_view(0, -0.1)

    def reset_view(self, event):
        self.a = 1.5
        self.slider_a.set_val(self.a)
        self.x_min, self.x_max = -self.a, self.a
        self.y_min, self.y_max = -self.a, self.a
        self.update_fractal()

if __name__ == "__main__":
    fractal = MandelbrotFractal()
    plt.show()
