from django.db import models

class Operacao(models.Model):
	TIPOS_OPERACAO = (('C', 'Compra'),('V', 'Venda'))
	TIPOS_TITULO = (
        ('I', 'IPCA'),
		('S', 'Selic'),
		('P', 'Prefixado'),
		('IJS', 'IPCA com Juros Semestrais'),
		('PJS', 'Prefixado com Juros Semestrais'),
    )

	tipo_operacao = models.CharField(max_length=16, choices=TIPOS_OPERACAO, default=None)
	valor_investido = models.FloatField(default=None, null=True)
	qnt_titulo = models.FloatField(default=None, null=True)
	tipo_titulo = models.CharField(max_length=48, choices=TIPOS_TITULO, default=None) 
	data_vencimento = models.DateTimeField(default=None)
	pu_compra = models.FloatField(default=None, null=True)
	data_operacao = models.DateTimeField(default=None)