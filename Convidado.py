from email.utils import parseaddr

class Convidado:
	def __init__(self, email, local):
		try:
			self.Email = self.validaEmail(email)
		except ValueError as e:
			print("Algo de errado aconteceu. {}".format(e))
		self.Local = local

	def validaEmail(self, email):
		testEmail = parseaddr(email)[1]

		if '@' not in testEmail:
			raise ValueError('E-mail inválido')

		return testEmail