from stn.models import Titulo, TituloAtivo
from warren.stncrawler import StnCrawler
from datetime import datetime

class StnPool():

	def __init__(self):
		self._poll = None
		self._pool_info = { 'criacao' : None, 'atualizacao' : None, 'tamanho' : None, 'chaves' : None }
		self._stncrawler = StnCrawler()
		self._idx = 0

	def carregar(self, keys):
		self._pool = Titulo.objects.filter(tipo_titulo=keys['tipo'], data_vencimento=keys['vencimento'], data_base__gte=keys['intervalo']).order_by('data_base')
		
		data_hora = datetime.now()

		self._pool_info = {
			'criacao' : datetime.strftime(data_hora,'%d/%m/%Y'),
			'atualizacao' : datetime.strftime(data_hora,'%H:%m'),
			'tamanho' : len(self._pool),
			'chaves' : keys
		}

	def recarregar(self):
		self.carregar(self._pool_info['keys'])

	def atualizar(self, keys):
		self.carregar(keys)

	def descarregar(self):
		self._poll = None
		self._pool_info = { 'creation' : None, 'update' : None, 'size' : None, 'keys' : None }

	def __str__(self):
		poolinfo = "_________________________________________\n"
		poolinfo += "Criação: {0} Atualização: {1}\n".format(self._pool_info['criacao'], self._pool_info['atualizacao'])
		poolinfo += "Tamanho: {0}\n".format(self._pool_info['tamanho'])
		poolinfo += "Chaves: {0} {1}\n".format(self._pool_info['chaves']['tipo'], self._pool_info['chaves']['vencimento'])
		poolinfo += "_________________________________________"

		return poolinfo

	def getTitulo(self):
		pass

	def getNext(self):
		if self._idx < self._pool_info['tamanho']:
			next_titulo = self._pool[self._idx]
			self._idx += 1

			return next_titulo

		else:
			return None