from django.shortcuts import render
from django.db.models import Count
from .forms import PessoaForm
from .models import Pessoa, PessoaFinalidade


def responder_pesquisa(request):

    if request.method == 'POST':
        form = PessoaForm(request.POST)

        if form.is_valid():
            pessoa = form.save()

            for finalidade in form.cleaned_data['finalidades']:
                PessoaFinalidade.objects.create(
                    pessoa=pessoa,
                    finalidade=finalidade
                )

            return render(
                request,
                'pesquisa/sucesso.html'
            )

    else:
        form = PessoaForm()

    return render(
        request,
        'pesquisa/pesquisa.html',
        {'form': form}
    )


def resultados(request):
    total_participantes = Pessoa.objects.count()

    participantes_por_faixa = (
        Pessoa.objects
        .values('faixa_etaria')
        .annotate(total=Count('id'))
        .order_by('faixa_etaria')
    )

    finalidades_mais_escolhidas = (
        PessoaFinalidade.objects
        .values('finalidade__nome')
        .annotate(total=Count('pessoa'))
        .order_by('-total')
    )

    finalidades_por_faixa = (
        PessoaFinalidade.objects
        .values(
            'pessoa__faixa_etaria',
            'finalidade__nome'
        )
        .annotate(total=Count('pessoa'))
        .order_by(
            'pessoa__faixa_etaria',
            '-total'
        )
    )

    faixas_nomes = {
        'ate-18': 'Até 18 anos',
        '19-30': '19 a 30 anos',
        '31-50': '31 a 50 anos',
        '51+': '51 anos ou mais',
    }

    for faixa in participantes_por_faixa:
        faixa['nome'] = faixas_nomes.get(
            faixa['faixa_etaria'],
            faixa['faixa_etaria']
        )

    for item in finalidades_por_faixa:
        item['nome_faixa'] = faixas_nomes.get(
            item['pessoa__faixa_etaria'],
            item['pessoa__faixa_etaria']
        )

    return render(
        request,
        'pesquisa/resultados.html',
        {
            'total_participantes': total_participantes,
            'participantes_por_faixa': participantes_por_faixa,
            'finalidades_mais_escolhidas': finalidades_mais_escolhidas,
            'finalidades_por_faixa': finalidades_por_faixa
        }
    )