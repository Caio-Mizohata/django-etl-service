from django.shortcuts import render, redirect
from django.contrib import messages
from consulta.apis.extrair_api import requisitar_dados
from consulta.services.transformar_service import escrever_csv_filtrado, escrever_csv_completo
from django.http import HttpResponse
from django.conf import settings


async def listar_municipios(request, state_code=settings.STATE_UF['UF']):

    dados_municipios = await requisitar_dados(state_code)
    
    if not dados_municipios or dados_municipios is None:
        messages.error(request, "Não foi possível obter os dados dos municípios")
        return redirect('error_page')  
    
    # Ordena por população decrescente (N/A fica no final)
    dados_municipios.sort(
        key=lambda x: x['populacao'] if x['populacao'] != 'N/A' else float('-inf'),
        reverse=True
    )
    
    # Prepara o contexto com dados adicionais
    contexto = {
        'municipios': dados_municipios,
        'uf': dados_municipios[0]['microrregiao']['mesorregiao']['UF'] if dados_municipios else {},
        'regiao': dados_municipios[0]['microrregiao']['mesorregiao']['UF']['regiao'] if dados_municipios else {},
        'state_code': state_code
    }
    
    return render(request, 'municipios.html', contexto)


async def baixar_csv_filtrado(request, state_code=settings.STATE_UF['UF']):
    arquivo_csv = await escrever_csv_filtrado(state_code)
    
    if not arquivo_csv or state_code is None:
        messages.error(request, "Falha ao gerar arquivo CSV")
        return redirect('error_page')
    
    # Configura a resposta com encoding UTF-8 para caracteres especiais
    response = HttpResponse(
        arquivo_csv.getvalue(),
        content_type='text/csv; charset=utf-8'
    )
    
    nome_arquivo = f"municipios_tratados_{state_code}.csv"
    
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    response['Cache-Control'] = 'no-cache'
    
    return response


async def baixar_csv_completo(request, state_code=settings.STATE_UF['UF']):
    arquivo_csv = await escrever_csv_completo(state_code)
    
    if not arquivo_csv or state_code is None:
        messages.error(request, "Falha ao gerar arquivo CSV completo.")
        return redirect('error_page')
    
    response = HttpResponse(
        arquivo_csv.getvalue(),
        content_type='text/csv; charset=utf-8'
    )

    nome_arquivo = f"total_municipios_{state_code}.csv"
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    response['Cache-Control'] = 'no-cache'
    
    return response


def download_page(request):
    return render(request, 'download.html')


def pagina_erro(request):
    mensagem = request.GET.get('mensagem')
    erro_download = request.GET.get('erro_download') == 'true'
    detalhes = request.GET.get('detalhes')

    context = {
        'mensagem': mensagem,
        'erro_download': erro_download,
        'debug': settings.DEBUG,
        'detalhes': detalhes,
    }
    
    return render(request, 'erro.html', context)
