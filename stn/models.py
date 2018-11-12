from django.db import models

class TituloAbstrato(models.Model):
	TIPOS_TITULO = (
        ('I', 'IPCA'),
		('S', 'Selic'),
		('P', 'Prefixado'),
		('IJS', 'IPCA com Juros Semestrais'),
		('PJS', 'Prefixado com Juros Semestrais'),
    )

	tipo_titulo = models.CharField(max_length=48, choices=TIPOS_TITULO, default=None)
	data_vencimento = models.DateTimeField(default=None)
	data_base = models.DateTimeField(default=None)
	taxa_compra = models.FloatField(default=None, null=True)
	taxa_venda = models.FloatField(default=None, null=True)
	pu_compra = models.FloatField(default=None, null=True)
	pu_venda = models.FloatField(default=None, null=True)
	pu_base = models.FloatField(default=None, null=True)

	class Meta:
		unique_together = ('tipo_titulo', 'data_vencimento', 'data_base')
		abstract = True

	def __str__(self):
		titulo_str = "Tipo: {tt} Vencimento: {dv}\nData: {db}\nTaxa Compra: {tc}\nTaxa Venda: {tv}\nPU Compra: {puc}\nPU Venda: {puv}"

		return titulo_str.format(
			tt=self.tipo_titulo,
			db=self.data_base,
			dv=self.data_vencimento.year,
			tc=self.taxa_compra,
			tv=self.taxa_venda,
			puc=self.pu_compra,
			puv=self.pu_venda
		)

class Titulo(TituloAbstrato):

	def __str__(self):
		return super(Titulo, self).__str__()

class TituloAtivo(TituloAbstrato):
	OPCOES = (
        ('C', 'compra'),
		('V', 'venda')
    )

	opcao = models.CharField(max_length=16, choices=OPCOES, default=None)

	def __str__(self):
		return super(TituloAtivo, self).__str__()
