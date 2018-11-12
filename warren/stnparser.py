import re
from html.parser import HTMLParser
from datetime import datetime, timedelta
from stn.models import Titulo, TituloAtivo
from warren.common import *

class StnParser(HTMLParser):

	def __init__(self):
		self._compra_dict = { '0' : 'tt', '1' : 'dv', '2' : 'tc', '3' : 'vm' , '4' : 'puc' }
		self._venda_dict = { '0' : 'tt', '1' : 'dv', '2' : 'tv', '3' : 'puv' }
		# [Título Novo, Compra ou Venda, Atributo]
		self._state = [False, 0, -1]
		self._titulo = None
		self._titulosCompra = []
		self._titulosVenda = []
		self._datetime_pattern = re.compile("(?P<dia>\d{2})\/(?P<mes>\d{2})\/(?P<ano>\d{4}) (?P<hora>\d{2}):(?P<min>\d{2})")
		self._stn_page_datetime = None

		super(StnParser, self).__init__()

	def handle_starttag(self, startTag, attrs):
		if startTag == 'td':
			for name, value in attrs:
				if name == 'class' and 'listing0' in value:
					self._titulo = {}
					self._state[0] = True
					self._state[2] += 1

				elif name == 'class' and 'listing' in value:
					self._state[0] = True
					self._state[2] += 1

		else:
			self._state[0] = False
			self._state[2] = -1

	def handle_data(self, data):
		stn_page_datetime = re.findall(self._datetime_pattern, data)

		if stn_page_datetime != []:
			self._stn_page_datetime = datetime.strptime(data, "%d/%m/%Y %H:%M")

		if data == " Investir ":
			self._state[1] = 0

		elif data == " Resgatar ":
			self._state[1] = 1

		if self._state[0] and data != ' ':
			if self._state[1] == 0:
				if self._state[2] != 3:
					self._titulo[self._compra_dict[str(self._state[2])]] = data
			else:
				self._titulo[self._venda_dict[str(self._state[2])]] = data

		if self._state[0]:
			if (self._state[1] == 0 and self._state[2] == 4) or \
			   (self._state[1] == 1 and self._state[2] == 3):
				self._titulo['db'] = datetime.now().strftime("%d/%m/%Y")
				self._titulo['tt'] = self._titulo['tt'][8:len(self._titulo['tt']) - 5]

				if self._state[1] == 0:
					self._titulo['puc'] = self._titulo['puc'].replace('R$', '')
					self._titulosCompra.append(self._titulo)
				else:
					self._titulo['puv'] = self._titulo['puv'].replace('R$', '')
					self._titulosVenda.append(self._titulo)
				#print(self._titulo)

				self._state[0] = False
				self._state[2] = -1

	def feed(self, data):
		super(StnParser, self).feed(data)

		return self._titulosCompra, self._titulosVenda, self._stn_page_datetime 

	def parse(self, data):
		return self.feed(data)