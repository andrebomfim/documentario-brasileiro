# Documentário Brasileiro — Raspagem de dados

Script em Python para raspagem da base de dados do site [documentariobrasileiro.com.br](http://documentariobrasileiro.com.br).

## Problema

O site Documentário Brasileiro reúne um acervo extenso de filmes documentais brasileiros, mas só permite pesquisa por título, diretor, década, gênero ou metragem. Não há busca por sinopse.

## Solução

O script raspa todos os registros da base — título, sinopse, direção, ano, duração, estado produtor, link do filme, fonte de pesquisa e link do cartaz — e os grava em um arquivo CSV, que pode ser importado para o Google Sheets ou Excel e pesquisado por qualquer campo, incluindo a sinopse.

## Funcionamento

O script percorre as páginas do catálogo, identifica os códigos de cada filme e acessa individualmente cada registro para extrair os dados. Os resultados são gravados de forma incremental em `docbrasil.csv` à medida que a raspagem avança.

## Campos extraídos

| Campo | Descrição |
|---|---|
| `titulo` | Título do filme |
| `sinopse` | Sinopse |
| `direcao` | Direção |
| `ano` | Ano de produção |
| `duracao` | Duração |
| `uf` | Estado produtor |
| `link_filme` | Link externo do filme |
| `link_base` | Link do registro na base |
| `codigo` | Código interno da base |
| `obs` | Observações |
| `fonte` | Fonte de pesquisa |
| `cartaz` | Link do cartaz |
| `raspagem` | Data e hora da extração |

## Requisitos

- Python 3.x
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

Instalação das dependências:

```bash
pip install requests beautifulsoup4
```

## Uso

```bash
python docbrasil.py
```

O script inicia a raspagem a partir da página 1. Para retomar de uma página específica, altere o parâmetro `p` na chamada da função `raspa_docbrasil()` no final do arquivo:

```python
raspa_docbrasil(p=150)
```

O progresso é exibido no terminal com o título de cada filme processado e timestamps de início e fim.

## Saída

Arquivo `docbrasil.csv` no diretório de execução, pronto para importação no Google Sheets ou em qualquer ferramenta de análise de dados.

## Observações

- O script usa sessão com cookies para simular navegação convencional.
- A gravação é incremental: em caso de interrupção, os dados já extraídos são preservados no CSV.
- O parâmetro `pmax` define o limite máximo de páginas a percorrer (padrão: 2000).

## Dados

A publicação dos dados extraídos em formato CSV foi autorizada por Katia Holanda, responsável pelo projeto e site documentariobrasileiro.com.br.
