from django.core.management.base import BaseCommand, CommandError
from warren.stncrawler import StnCrawler
from datetime import datetime
from stn.models import TituloAtivo

class Command(BaseCommand):
	help = 'Simulação de estratégia'

	def add_arguments(self, parser):
		parser.add_argument('tipo', type=str, help='Tipo de título')
		parser.add_argument('vencimento', type=str, help='Data de vencimento')

	def handle(self, *args, **options):
		info = {
			'tipo' : options['tipo'],
			'vencimento' : datetime.strptime(options['vencimento'], '%d/%m/%Y')
		}

		crawler = StnCrawler()
		t_compra, t_venda, datahora = crawler.crawling()

		for t in t_compra:
			titulo = TituloAtivo(
				tipo_titulo = t['tt'],
				data_vencimento = datetime.strptime(t['dv'], '%d/%m/%Y'),
				data_base = datetime.strptime(t['db'], '%d/%m/%Y'),
				taxa_compra = eval(t['tc'].replace('.', '').replace(',', '.')),
				pu_compra = eval(t['puc'].replace('.', '').replace(',', '.')),
				opcao='compra'
			)

			try:
				titulo.save()
			except:
				pass

		for t in t_venda:
			titulo = TituloAtivo(
				tipo_titulo = t['tt'],
				data_vencimento = datetime.strptime(t['dv'], '%d/%m/%Y'),
				data_base = datetime.strptime(t['db'], '%d/%m/%Y'),
				taxa_venda = eval(t['tv'].replace('.', '').replace(',', '.')),
				pu_venda = eval(t['puv'].replace('.', '').replace(',', '.')),
				opcao='venda'
			)

			try:
				titulo.save()
			except:
				pass