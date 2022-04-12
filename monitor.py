import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import tkinter.ttk as ttk

class Monitor(object):
	def __init__(self, nodes, xlim, ylim, length):
		self.window = tk.Tk()
		self.window.attributes('-type', 'dialog')

		self.nodes = nodes
		self.n = len(nodes)
		self.xlim = xlim
		self.ylim = ylim
		self.length = length

		plt.ion()
		self.fig, self.ax = plt.subplots(figsize=(8, 8))

		chart = FigureCanvasTkAgg(self.fig, self.window)
		chart.get_tk_widget().grid(row=0, column=0, sticky="nsw")

		self.ax.set_xlim(xlim)
		self.ax.set_ylim(ylim)
		self.lines = []
		for x, y in nodes:
			line, = self.ax.plot([x, x], [y, y])
			self.lines.append(line)

		self.frm_panel = ttk.Frame(master=self.window)

		self.frm_switch = ttk.Frame(master=self.frm_panel)
		self.lbl_switch = ttk.Label(master=self.frm_switch, text="on")
		self.btn_switch = ttk.Button(master=self.frm_switch, text="switch")
		self.lbl_switch.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
		self.btn_switch.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

		self.frm_switch.pack()
		self.frm_panel.grid(row=0, column=1, sticky="new")

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
	
	def update(self):
		self.window.update()
