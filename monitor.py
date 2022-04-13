import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import tkinter.ttk as ttk

class Monitor(object):
	def __init__(self, nodes, xlim, ylim, length):
		self.window = tk.Tk()

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

		self.mode = tk.IntVar()
		self.mode.set(0)
		self.init_ui()

		self.switch_status = True

	def init_ui(self):
		self.window.attributes('-type', 'dialog')

		chart = FigureCanvasTkAgg(self.fig, self.window)
		chart.get_tk_widget().grid(row=0, column=0, sticky="nsw")

		self.frm_panel = tk.Frame(master=self.window)

		# switch on/off
		self.frm_switch = tk.Frame(master=self.frm_panel)
		self.lbl_switch = tk.Label(master=self.frm_switch, text="on")
		self.btn_switch = tk.Button(master=self.frm_switch, text="switch", command=self.switch)
		self.lbl_switch.grid(row=0, column=0, sticky="ew", padx=5)
		self.btn_switch.grid(row=1, column=0, sticky="ew", padx=5)

		# switch mode
		self.frm_mode = tk.Frame(master=self.frm_panel)
		self.lbl_mode = tk.Label(master=self.frm_mode, text="mode")
		self.rdo_auto = tk.Radiobutton(master=self.frm_mode, text="auto", variable=self.mode, value=0)
		self.rdo_manual = tk.Radiobutton(master=self.frm_mode, text="manual", variable=self.mode, value=1)
		self.rdo_learn = tk.Radiobutton(master=self.frm_mode, text="learn", variable=self.mode, value=2)
		self.rdo_detect = tk.Radiobutton(master=self.frm_mode, text="detect", variable=self.mode, value=3)
		self.lbl_mode.grid(row=0, column=0, sticky="ew", padx=5)
		self.rdo_auto.grid(row=1, column=0, sticky="w", padx=5)
		self.rdo_manual.grid(row=2, column=0, sticky="w", padx=5)
		self.rdo_learn.grid(row=3, column=0, sticky="w", padx=5)
		self.rdo_detect.grid(row=4, column=0, sticky="w", padx=5)

		# history
		self.frm_history = tk.Frame(master=self.frm_panel)
		# self.lbl_history = tk.Lable(master=self.frm_history, text="history")
		self.btn_history = tk.Button(master=self.frm_history, text="history")
		self.btn_history.grid(row=0, column=0, sticky="ew", padx=5)

		# developer
		self.frm_develop = tk.Frame(master=self.frm_panel)
		# self.lbl_history = tk.Lable(master=self.frm_history, text="history")
		self.btn_develop = tk.Button(master=self.frm_develop, text="develop")
		self.btn_develop.grid(row=0, column=0, sticky="ew", padx=5)

		self.frm_switch.grid(row=0, column=0, padx=5, pady=5)
		self.frm_mode.grid(row=1, column=0, padx=5, pady=5)
		self.frm_history.grid(row=2, column=0, padx=5, pady=5)
		self.frm_develop.grid(row=3, column=0, padx=5, pady=5)
		self.frm_panel.grid(row=0, column=1, sticky="new")


	def plot(self, angles):
		if not self.switch_status:
			return
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
		if not self.switch_status:
			self.clear()
		self.window.update()

	def switch(self):
		self.switch_status = not self.switch_status
		self.lbl_switch['text'] = { True: "on", False: "off"}[self.switch_status]
