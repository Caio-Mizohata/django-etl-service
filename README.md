# 🚀 Projeto ETL de Dados de Municípios Brasileiros 🇧🇷  

Aplicação Web desenvolvida com **Django** para **Extrair, Transformar e Visualizar (ETL)** dados **demográficos e geográficos** de municípios do Brasil, utilizando **APIs públicas**.  

## 👨‍💻 Autores
- **Caio Mizohata**
- **Guilherme de Barros**

--- 

## 📖 Sobre o Projeto

O projeto consiste em uma Aplicação Web que extrai dados de fontes públicas (API do IBGE e Wikidata), realiza a transformação e limpeza desses dados (como normalização de texto e combinação de fontes), e os disponibiliza para:
1.  **Visualização** em uma interface web amigável.
2.  **Download** em formato CSV, com opções de dados filtrados ou completos.

Este projeto foi desenvolvido como parte da disciplina de `[Gestão de dados]` do curso de `[Big Data no Agronegócio]` na `[Fatec Pompeia Shunji Nishimura]`.

## 📂 Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
trabalho_ETL/
├── app/              # Configurações do framework (coração do projeto)
├── consulta/         # App principal do Django
│   ├── apis/         # Lógica para extração de dados (extrair_api.py)
│   ├── services/     # Lógica de negócio e transformação (transformar_service.py)
│   ├── templates/    # Templates HTML
│   └── views.py      # Controladores que lidam com as requisições
├── home/             # App para a página inicial
├── static/           # Arquivos estáticos (CSS, JS, imagens)
└── trabalho_ETL/     # Configurações do projeto Django (settings.py, urls.py)
```
---

## ✨ Funcionalidades  

✔️ **Extração de dados** via:  
- 📡 **API do IBGE** → informações administrativas e geográficas.  
- 🌐 **Wikidata (SPARQL)** → dados populacionais.  

✔️ **Transformação de dados**:  
- Normalização de nomes (remoção de acentos e caracteres especiais).  
- Cálculo da média populacional.  
- Combinação de dados entre fontes diferentes.  

✔️ **Visualização interativa**:  
- Tabela moderna, pesquisável e responsiva com os municípios e dados tratados.  

✔️ **Exportação (Carga)** em `.csv`:  
- **Filtrado** → municípios acima da média populacional.  
- **Completo** → todos os municípios, tratados e combinados.  

---

## 🛠️ Tecnologias Utilizadas  

- **Backend**: Django + Python  
- **Frontend**: HTML5, CSS3, JavaScript  
- **APIs**: `httpx` para requisições assíncronas  
- **Manipulação de dados**: Python (`csv`, `unicodedata`, `re`)  

---

## 🚀 Executando o Projeto

Para executar este projeto, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Caio-Mizohata/django-etl-service.git
    cd django-etl-service
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor de desenvolvimento do Django:**
    ```bash
    python manage.py runserver
    ```

5.  **Acesse a aplicação** no seu navegador em `http://127.0.0.1:8000/`.
