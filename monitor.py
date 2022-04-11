import math
import matplotlib as mpl
import matplotlib.pyplot as plt

class Monitor(object):
	def __init__(self, nodes, xlim, ylim, length):
		self.nodes = nodes
		self.n = len(nodes)
		self.xlim = xlim
		self.ylim = ylim
		self.length = length

		plt.ion()
		self.fig, self.ax = plt.subplots(figsize=(8, 8))
		self.ax.set_xlim(xlim)
		self.ax.set_ylim(ylim)
		self.lines = []
		for x, y in nodes:
			line, = self.ax.plot([x, x], [y, y])
			self.lines.append(line)

	def plot(self, angles):
		if len(angles) != self.n:
			raise ValueError("Angle list length incorrect")
		for i in range(self.n):
			x, y = self.nodes[i]
			angle = angles[i]

			endx = x + self.length * math.cos(angle)
			endy = y + self.length * math.sin(angle)

			self.lines[i].set_xdata([x, endx])
			self.lines[i].set_ydata([y, endy])

			self.ax.plot(x, y, marker="o", markersize=4)

		self.draw()
			

	def draw(self):
		self.fig.canvas.draw()
		self.fig.canvas.flush_events()
