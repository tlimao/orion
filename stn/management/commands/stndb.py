from django.core.management.base import BaseCommand, CommandError
from stn.models import Titulo
from datetime import datetime
import urllib.request
import ssl

class Command(BaseCommand):
    help = 'Cria e popula o banco com dados históricos dos títulos do tesouro'

    STN_FILE = "stn/management/commands/data/PrecoTaxaTesouroDireto.csv"
    STN_URL = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"

    CONSTRAINT = 'IGPM+'

    def add_arguments(self, parser):
        parser.add_argument('ação', type=str, help='Criar, Atualizar ...')

    def handle(self, *args, **options):
        start_time = datetime.now()

        if options['ação'] ==  'create':
            msg = 'Banco CRIADO com sucesso!\nDuração '

        elif options['ação'] == 'update':
            msg = 'Banco ATUALIZADO com sucesso!\nDuração '
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            u = urllib.request.urlopen(self.STN_URL, context=ctx)
            f = open(self.STN_FILE, 'wb')
            f.write(u.read())

            f.close()

        f = open(self.STN_FILE, 'r')

        lines = f.readlines()[1:]
        data_hoje = datetime.now()

        for line in lines:
            if line != '':

                values = line.replace('\n','').split(';')

                if self.CONSTRAINT not in values[0] and values[7] != '' and datetime.strptime(values[1], '%d/%m/%Y').year > data_hoje.year:
                    titulo = Titulo(
                        tipo_titulo = values[0][8:].replace('+', ''),
                        data_vencimento = datetime.strptime(values[1], '%d/%m/%Y'),
                        data_base = datetime.strptime(values[2], '%d/%m/%Y'),
                        taxa_compra = eval(values[3].replace('.', '').replace(',', '.')),
                        taxa_venda = eval(values[4].replace('.', '').replace(',', '.')),
                        pu_compra = eval(values[5].replace('.', '').replace(',', '.')),
                        pu_venda = eval(values[6].replace('.', '').replace(',', '.')),
                        pu_base = eval(values[7].replace('.', '').replace(',', '.'))
                    )

                    try:
                        titulo.save()
                    except:
                        pass

        f.close()
        end_time = datetime.now()

        self.stdout.write(self.style.SUCCESS(msg + str(end_time - start_time)))