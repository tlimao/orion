from django.http import HttpResponse
from django.template import loader
from django.views import View
from datetime import datetime, timedelta
from warren.stnpool import StnPool
from warren.indicadores import MML
import json

class BoxView(View):

	def get(self, request):
		if request.is_ajax():
			Id = request.GET['id']

			info = {
				'tipo' : request.GET['tipo'],
				'vencimento' : datetime.strptime(request.GET['vencimento'], '%d/%m/%Y'),
				'intervalo' : datetime.now() + timedelta(days=-int(request.GET['periodo']))
			}
			print(info)
			pool = StnPool()
			pool.carregar(info)
			mml = MML(20)

			context = { 'data_plot' : { 'datetime' : [], 'preco' : [] }}

			titulo = pool.getNext()

			while titulo != None:
				mml.push((titulo.data_base, titulo.pu_compra))
				context['data_plot']['datetime'].append(datetime.strftime(titulo.data_base, '%m/%Y'))
				context['data_plot']['preco'].append(titulo.pu_compra)

				titulo = pool.getNext()

			context['data_plot']['mml'] = mml.getDataArray()['yaxis']

			return HttpResponse(json.dumps(context))

		else:
			template = loader.get_template('box/chart.html')

			return HttpResponse(template.render(None, request))