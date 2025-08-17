from django.conf import settings
import unicodedata, csv, re
from io import StringIO
from consulta.apis.extrair_api import requisitar_dados


def formatar_texto_csv(text):
    if not text:
        return ''
    
    # Converte para caixa baixa
    text = text.lower()
    # Remove acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Remove caracteres especiais (exceto espaços e letras)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Remove espaços extras
    text = ' '.join(text.split())
    return text


async def escrever_csv_filtrado(state_code=settings.STATE_UF['UF']):
    dados_municipios = await requisitar_dados(state_code)
    
    if not dados_municipios:
        return None
    
    # Realiza um pré-processamento e normalização
    for municipio in dados_municipios:
        municipio['nome_normalizado'] = formatar_texto_csv(municipio['nome'])
    
    # Calcula a média populacional (excluindo 'N/A')
    populacoes = [municipio['populacao'] for municipio in dados_municipios if isinstance(municipio['populacao'], int)]
    media_populacao = sum(populacoes) / len(populacoes) if populacoes else 0
    
    # Filtra municípios acima da média e prepara dados para CSV
    municipios_filtrados = []
    for municipio in dados_municipios:
        if isinstance(municipio['populacao'], int) and municipio['populacao'] > media_populacao:
            municipios_filtrados.append({
                'codigo_ibge': municipio['codigo_ibge'],
                'nome': municipio['nome_normalizado'],  
                'populacao': municipio['populacao']
            })
    
    # Ordena por população decrescente
    municipios_filtrados.sort(key=lambda x: x['populacao'], reverse=True)
    
    # Cria o arquivo CSV em memória
    output = StringIO()
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
    
    # Escreve o cabeçalho
    writer.writerow([
        'codigo_ibge',
        'nome_cidade',
        'populacao_estimada'
    ])
    
    # Escreve dados filtrados
    for city in municipios_filtrados:
        writer.writerow([
            city['codigo_ibge'],
            city['nome'],
            city['populacao']
        ])
    
    output.seek(0)
    return output


async def escrever_csv_completo(state_code=settings.STATE_UF['UF']):
    dados_municipios = await requisitar_dados(state_code)
    if not dados_municipios:
        return None

    # Pré-processamento e normalização
    for municipio in dados_municipios:
        municipio['nome_normalizado'] = formatar_texto_csv(municipio['nome'])

    # Cria o arquivo CSV em memória
    output = StringIO()
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')

    # Escreve cabeçalho com todos os campos
    writer.writerow([
        'codigo_ibge',
        'nome_cidade',
        'populacao_estimada',
        'microrregiao_id',
        'microrregiao_nome',
        'mesorregiao_id',
        'mesorregiao_nome',
        'uf_id',
        'uf_sigla',
        'uf_nome',
        'regiao_id',
        'regiao_sigla',
        'regiao_nome'
    ])

    # Escreve todos os dados
    for city in dados_municipios:
        writer.writerow([
            city.get('codigo_ibge'),
            city.get('nome_normalizado'),
            city.get('populacao'),
            city['microrregiao']['id'],
            city['microrregiao']['nome'],
            city['microrregiao']['mesorregiao']['id'],
            city['microrregiao']['mesorregiao']['nome'],
            city['microrregiao']['mesorregiao']['UF']['id'],
            city['microrregiao']['mesorregiao']['UF']['sigla'],
            city['microrregiao']['mesorregiao']['UF']['nome'],
            city['microrregiao']['mesorregiao']['UF']['regiao']['id'],
            city['microrregiao']['mesorregiao']['UF']['regiao']['sigla'],
            city['microrregiao']['mesorregiao']['UF']['regiao']['nome']
        ])

    output.seek(0)
    return output


if __name__ == '__main__':
    import asyncio

    async def main():
        print("Testando: escrever_csv_filtrado")
        await escrever_csv_filtrado()
        print("Testando: escrever_csv_completo")
        await escrever_csv_completo()

    asyncio.run(main())
    