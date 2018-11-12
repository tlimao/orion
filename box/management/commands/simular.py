from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from warren.stnpool import StnPool
from warren.indicadores import MML

class Command(BaseCommand):
	help = 'Simulação de estratégia'

	def add_arguments(self, parser):
		parser.add_argument('id', type=str, help='Id para simulação')
		parser.add_argument('tipo', type=str, help='Tipo de título')
		parser.add_argument('vencimento', type=str, help='Data de vencimento')
		parser.add_argument('intervalo', type=int, help='Intervalo de tempo')

	def handle(self, *args, **options):
		info = {
			'tipo' : options['tipo'],
			'vencimento' : datetime.strptime(options['vencimento'], '%d/%m/%Y'),
			'intervalo' : datetime.now() + timedelta(days=-options['intervalo'])
		}

		pool = StnPool()
		pool.carregar(info)
		mml = MML(50)

		preco_data = [[], []]

		titulo = pool.getNext()

		while titulo != None:
			mml.push((titulo.data_base, titulo.pu_compra))
			preco_data[0].append(titulo.data_base)
			preco_data[1].append(titulo.pu_compra)

			titulo = pool.getNext()

		# Plotar Gráfico
		years = mdates.MonthLocator()
		#months = mdates.DayLocator()
		yearsFmt = mdates.DateFormatter('%m-%Y')

		fig, ax = plt.subplots()
		mml_data = mml.getDataArray()

		ax.plot(mml_data['xaxis'], mml_data['yaxis'], label="MML")
		ax.plot(preco_data[0], preco_data[1], label=options['tipo'] + " " + options['vencimento'])

		ax.xaxis.set_major_locator(years)
		ax.xaxis.set_major_formatter(yearsFmt)
		#ax.xaxis.set_minor_locator(months)

		datemin = np.datetime64(mml_data['xaxis'][-1], 'M')
		datemax = np.datetime64(mml_data['xaxis'][0], 'M') + np.timedelta64(1, 'M')
		
		ax.set_xlim(datemin, datemax)
		ax.format_xdata = mdates.DateFormatter('%d/%m/%Y')

		plt.xticks(rotation=70)
		plt.legend()
		plt.show()