import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Dplot(object):
    def __init__(self, npoints: int, x_label: str, y_label: str, title: str, data: list):
        self.npoints = npoints

        if (type(data) == list and len(data) > 0):
            self.x = deque([x for x in range(len(data))], maxlen=npoints)
            self.y = deque(data, maxlen=npoints)
        else:
            self.x = deque([0], maxlen=npoints)
            self.y = deque([0], maxlen=npoints)
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        [self.line] = self.ax.step(self.x, self.y)

    def _update(self, dy):
        self.x.append(self.x[-1] + 1)  # update data
        self.y.append(dy)

        self.line.set_xdata(self.x)  # update plot data
        self.line.set_ydata(self.y)

        self.ax.relim()  # update axes limits
        self.ax.autoscale_view(True, True, True)
        return self.line, self.ax

    def data_gen(self):
        while True:
            yield float(random.randint(-10,10)) # вместо рандома вставить функцию, возвпащающую новые значения

    def draw(self):
        ani = animation.FuncAnimation(self.fig, self._update, self.data_gen)
        plt.show()

if __name__ == '__main__':
    my_plot = Dplot(100, 'x', 'y', 'title', [random.random() for x in range(40)])
    my_plot.draw()