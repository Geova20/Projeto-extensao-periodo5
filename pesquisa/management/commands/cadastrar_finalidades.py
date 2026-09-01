from django.core.management.base import BaseCommand
from pesquisa.models import Finalidade


class Command(BaseCommand):
    help = 'Cadastra as finalidades da pesquisa'

    def handle(self, *args, **options):
        finalidades = [
            'Informação e notícias',
            'Entretenimento',
            'Comunicação',
            'Estudo',
            'Trabalho',
            'Compras e serviços',
            'Serviços financeiros',
            'Outro',
        ]

        for nome in finalidades:
            Finalidade.objects.get_or_create(nome=nome)

        self.stdout.write(
            self.style.SUCCESS('Finalidades cadastradas com sucesso.')
        )
