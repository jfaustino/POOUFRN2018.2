import tkinter as tk

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master, height=600, width=800)
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.fr1 = tk.Frame(self, width=400, height=480)
		self.fr1.pack(side="left")
		self.fr2 = tk.Frame(self, width=400, height=480)
		self.fr2.pack(side="right")
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello, world\n(click me)"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack()

		self.quit = tk.Button(self, text="Quit", fg="red",
			command=root.destroy)
		self.quit.pack()

	def say_hi(self):
		print("Hi, there, everyone")

root = tk.Tk()
app = Application(master=root)
app.master.minsize(800, 480)
app.mainloop()