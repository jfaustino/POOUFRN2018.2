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
				dtHoraInicio, dtHoraFim, anfitriao, localId)""")

			self.frEventos = tk.Frame(self, width=800, height=480)
			self.frEventos.pack()
			self.mainLabel["text"] = "Eventos"
			self.btAdicEvento = tk.Button(self.frEventos, text="Adicionar",
				command=partial(self.alteraEvento, "a"))
			self.btAdicEvento.pack(side="left")
			self.btEditarEvento = tk.Button(self.frEventos, text="Editar",
				command=partial(self.alteraEvento, "e"))
			self.btEditarEvento.pack(side="top")
			self.btRemoverEvento = tk.Button(self.frEventos, text="Remover",
				command=partial(self.alteraEvento, "r"))
			self.btRemoverEvento.pack(side="right")
		# elif perfil == 1:
		# 	self.frConvDetalhes = tk.Frame(self, width=800, height=480)
		# 	self.frConvDetalhes.pack()

	def alteraEvento(self, acao):
		# TODO
		if acao == "a":
			self.frEventos.pack_forget()
			self.frDetalheEvento = tk.Frame(self, width=800, height=480)

			# Label e entry dtHoraInicio
			self.frArea1 = tk.Frame(self.frDetalheEvento, width=800, bd=4).grid(row=0, column=0)
			self.lbDtHoraInicio = tk.Label(self.frArea1,
				text="Data e hora de início")
			self.lbDtHoraInicio.pack(side="left")
			self.enDtHoraInicio = tk.Entry(self.frArea1)
			self.enDtHoraInicio.pack(side="right")

			# Label e entry dtHoraFim
			self.frArea2 = tk.Frame(self.frDetalheEvento, width=800).grid(row=1, column=0)
			self.lbDtHoraFim = tk.Label(self.frArea2,
				text="Data e hora de término")
			self.lbDtHoraFim.pack(side="left")
			self.enDtHoraFim = tk.Entry(self.frArea2)
			self.enDtHoraFim.pack(side="right")

			# Label e entry anfitriao
			self.frArea3 = tk.Frame(self.frDetalheEvento, width=800).grid(row=2, column=0)
			self.lbAnfitriao = tk.Label(self.frArea3,
				text="E-mail anfitrião")
			self.lbAnfitriao.pack(side="left")
			self.enAnfitriao = tk.Entry(self.frArea3)
			self.enAnfitriao.pack(side="right")

			# Label e entry local
			self.frArea4 = tk.Frame(self.frDetalheEvento, width=800).grid(row=3, column=0)
			self.lbLocal = tk.Label(self.frArea4,
				text="Local")
			self.lbLocal.pack(side="left")
			self.enLocal = tk.Entry(self.frArea4)
			self.enLocal.pack(side="right")

			# Se o local não estiver na base de dados, assumir UTC +0
			query = """INSERT OR IGNORE INTO
			eventos (dtHoraInicio, dtHoraFim, anfitriao, localId)
			VALUES (?, ?, ?, ?)"""

			self.btAdicionar = tk.Button(self.frDetalheEvento, text="Salvar",
				command=partial(self.executaQuery, query,
					self.enDtHoraInicio.get(), self.enDtHoraFim.get(),
					self.enAnfitriao.get(), self.enLocal.get())).grid(
						row=4, column=0
					)

			self.frDetalheEvento.pack()
		#elif acao == "e":
		#elif acao == "r":

	def executaQuery(self, query, *args):
		dtInicio = args[0]
		dtFim = args[1]
		anfitriao = args[2]
		localId = self.buscaLocal(args[3])
		self.cur.execute(query, dtInicio, dtFim, anfitriao, localId)
		self.conn.commit()
	
	def buscaLocal(self, local):
		local = local.strip('\'\"\\;.')
		query = """SELECT geoNameId
		FROM cities
		WHERE name LIKE '%{}%';""".format(local)
		self.cur.execute(query)
		localId = self.cur.fetchone()

		if localId is None:
			localId = 0
	
		return localId

	def buscaTZ(self, localId):
		query = """SELECT timezone
		FROM cities
		WHERE geoNameId = {}""".format(localId)
		self.cur.execute(query)
		timezone = self.cur.fetchone()

		return timezone

root = tk.Tk()
app = Application(master=root)
app.master.minsize(800, 480)
app.mainloop()
app.conn.close()