from hashlib import sha512
from email.utils import parseaddr
import datetime as dt

class Convidado:
	def __init__(self, email, local):
		try:
			self.Email = self.validaEmail(email)
		except ValueError as e:
			print("Algo de errado aconteceu. {}".format(e))
		self.Local = local
		curDate = dt.datetime.now(dt.timezone.utc).isoformat()
		self.Id = sha512((self.Email + curDate).encode('utf-8')).hexdigest()

	def validaEmail(self, email):
		testEmail = parseaddr(email)[1]

		if '@' not in testEmail:
			raise ValueError('E-mail inválido')

		return testEmail