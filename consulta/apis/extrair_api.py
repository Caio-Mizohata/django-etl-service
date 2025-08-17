from django.conf import settings
from django.shortcuts import redirect
import httpx


async def requisitar_dados(state_code=settings.STATE_UF['UF']):
    sparql_config = settings.SPARQL_REQUEST_CONFIG
    state_codes = sparql_config['STATE_CODES']
    sparql_code = state_codes.get(state_code)

    if sparql_code is None:
        return redirect('error_page')

    sparql_query = f"""
    SELECT ?municipioLabel ?populacao WHERE {{
        ?municipio wdt:P31 wd:Q3184121;       
                  wdt:P131 wd:{sparql_code};           
                  wdt:P1082 ?populacao.       

        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pt,en". }}
    }}
    ORDER BY DESC(?populacao)
    """
    
    wikidata_dados = {}

    async with httpx.AsyncClient(timeout=sparql_config['TIMEOUT']) as client:
        try:
            # 1. Obter dados do Wikidata
            wikidata_response = await client.get(
                sparql_config['ENDPOINT'],
                params={'query': sparql_query, 'format': 'json'},
                headers={
                    'User-Agent': sparql_config['USER_AGENT'],
                    'Accept': 'application/json'
                }
            )
            wikidata_response.raise_for_status()

            for item in wikidata_response.json().get('results', {}).get('bindings', []):
                municipio_label = item.get('municipioLabel', {}).get('value', '')
                wikidata_dados[municipio_label] = {
                    'populacao': int(item.get('populacao', {}).get('value', 0))
                }

        except Exception as e:
            print(f"Erro ao consultar Wikidata: {str(e)}")
            return None

        # 2. Obter dados do IBGE
        try:
            ibge_url = f"{settings.API_IBGE_CONFIG['ENDPOINT']}/{state_code}/municipios"
            ibge_response = await client.get(
                ibge_url,
                headers={'User-Agent': settings.STATE_UF['UF']}
            )
            ibge_response.raise_for_status()
            ibge_data = ibge_response.json()

            # 3. Combinar os dados
            dados_combinados = []
            for municipio in ibge_data:
                nome_municipio = municipio.get('nome', '')
                wikidata_data = wikidata_dados.get(nome_municipio, {})

                microrregiao = municipio.get('microrregiao') or {}
                mesorregiao = microrregiao.get('mesorregiao') or {}
                uf = mesorregiao.get('UF') or {}
                regiao = uf.get('regiao') or {}

                dados_combinados.append({
                    'nome': nome_municipio,
                    'codigo_ibge': str(municipio.get('id', '')),

                    # Dados populacionais (Wikidata)
                    'populacao': wikidata_data.get('populacao', 'N/A'),
                    
                    # Estrutura geográfica (IBGE)
                    'microrregiao': {
                        'id': microrregiao.get('id'),
                        'nome': microrregiao.get('nome'),
                        'mesorregiao': {
                            'id': mesorregiao.get('id'),
                            'nome': mesorregiao.get('nome'),
                            'UF': {
                                'id': uf.get('id'),
                                'sigla': uf.get('sigla'),
                                'nome': uf.get('nome'),
                                'regiao': {
                                    'id': regiao.get('id'),
                                    'sigla': regiao.get('sigla'),
                                    'nome': regiao.get('nome')
                                }
                            }
                        }
                    }
                })
            
            return dados_combinados

        except httpx.RequestError as e:
            print(f"Erro ao acessar API do IBGE: {str(e)}")
            return None
        except Exception as e:
            print(f"Erro ao processar dados combinados: {str(e)}")
            return None


if __name__ == '__main__':
    import asyncio
    asyncio.run(requisitar_dados())
