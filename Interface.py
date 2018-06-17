from functools import partial
import sqlite3
import tkinter as tk

class Application(tk.Frame):
	conn = sqlite3.connect("test.db")
	cur = conn.cursor()

	def __init__(self, master=None):
		super().__init__(master, height=600, width=800)
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		# Rótulo principal
		self.mainLabel = tk.Label(self, text="Selecione seu perfil")
		self.mainLabel.pack()

		# Frames do anfitrião e do convidado
		self.frAnfitriao = tk.Frame(self, width=400, height=480)
		self.frAnfitriao.pack(side="left")
		self.frConvidado = tk.Frame(self, width=400, height=480)
		self.frConvidado.pack(side="right")

		# Seleção de perfil
		self.btAnfit = tk.Button(self.frAnfitriao, text="Anfitrião")
		self.btAnfit["command"] = partial(self.selecionaPerfil, 0)
		self.btAnfit.pack()
		self.btConv = tk.Button(self.frConvidado, text="Convidado")
		self.btConv["command"] = partial(self.selecionaPerfil, 1)
		self.btConv.pack()

	def selecionaPerfil(self, perfil):
		self.frAnfitriao.pack_forget()
		self.frConvidado.pack_forget()

		if perfil == 0:
			self.cur.execute("""CREATE TABLE IF NOT EXISTS eventos(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				dtHoraInicio, dtHoraFim, anfitriao, localId""")

			self.frEventos = tk.Frame(self, width=800, height=480)
			self.frEventos.pack()

			self.mainLabel["text"] = "Eventos"
			self.btAdicEvento = tk.Button(self.frEventos,
				command=partial(self.alteraEvento, "a"))
			self.btEditarEvento = tk.Button(self.frEventos,
				command=partial(self.alteraEvento, "e"))
			self.btRemoverEvento = tk.Button(self.frEventos,
				command=partial(self.alteraEvento, "r"))
		elif perfil == 1:
			self.frConvDetalhes = tk.Frame(self, width=800, height=480)
			self.frConvDetalhes.pack()

	def alteraEvento(self, acao):
		# TODO
		#if acao == "a":
		#elif acao == "e":
		#elif acao == "r":
		return

	def buscaLocal(self, local):
		local = local.strip('\'\"\\;.')
		queryLocal = "SELECT * FROM cities WHERE name LIKE %{}%;".format(local)
		result = self.cur.execute(queryLocal)
	
		return result

root = tk.Tk()
app = Application(master=root)
app.master.minsize(800, 480)
app.mainloop()