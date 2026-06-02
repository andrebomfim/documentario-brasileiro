import requests, csv, time
from bs4 import BeautifulSoup as BS


class Filme:

    def __init__(self,
                 titulo,
                 sinopse,
                 direcao,
                 ano,
                 duracao,
                 estado,
                 link_filme,
                 link_base,
                 codigo,
                 obs,
                 fonte,
                 cartaz):
        self.titulo = titulo
        self.sinopse = sinopse
        self.direcao = direcao
        self.ano = ano
        self.duracao = duracao
        self.estado = estado
        self.link_filme = link_filme
        self.link_base = link_base
        self.codigo = codigo
        self.obs = obs
        self.fonte = fonte
        self.cartaz = cartaz



class Colecao:

    def __init__(self):
        self.colecao = []

    def incluir_filme(self, filme):
        self.colecao.append(filme)

    def contar(self):
        print(f'{len(self.colecao)} filmes')

    def listar(self):
        lista = []
        for i in self.colecao:
            lista.append(i.titulo)
        print(sorted(lista))



def raspa_docbrasil(p=1, pmax=2000):

    print(f'\n{time.strftime("%d/%m/%Y %H:%M:%S")} - iniciando raspagem da base...')

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
               'Connection': 'keep-alive',
               'Host': 'documentariobrasileiro.com.br',
               'Sec-GPC': '1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:86.0) Gecko/20100101 Firefox/86.0'}
    session = requests.Session()
    url_inicio = 'http://documentariobrasileiro.com.br/'
    html_inicio = session.get(url_inicio, headers=headers)
    cookies = html_inicio.cookies

    for p in range(p, pmax):
        try:
            if p == 1:
                grava_cabecalho()
            else:
                pass
            urlp = 'http://documentariobrasileiro.com.br/catalogo/listar/p/' + str(p)
            htmlp = session.get(urlp, headers=headers, cookies=cookies)
            sopap = BS(htmlp.content, 'html.parser')
            tabelap = sopap.find('table', {'id': 'list-results'})
            resultadosp = tabelap.find_all('tr')
            for idfilme in resultadosp:
                try:
                    idfilme = idfilme['onclick'].strip('buscar(').strip(');')
                    raspa_filme(idfilme, session, headers, cookies)
                except KeyError:
                    pass
        except Exception as Err:
            print(f'\n{time.strftime("%d/%m/%Y %H:%M:%S")} - erro: {Err}\n')
            break

    print(f'{time.strftime("%d/%m/%Y %H:%M:%S")} - raspagem finalizada na pagina {p}.')


def raspa_filme(idfilme, session, headers, cookies):

    urlfilme = 'http://documentariobrasileiro.com.br/catalogo/filme/codigo/' + idfilme
    htmlfilme = session.get(urlfilme, headers=headers, cookies=cookies)
    sopafilme = BS(htmlfilme.content, 'html.parser')
    tabelafilme = sopafilme.find('div', {'class': 'panel-body'})
    try:
        titulo = tabelafilme.find('h2').text
    except AttributeError:
        titulo = None
    try:
        sinopse = tabelafilme.find_all('div', {'class': 'col-lg-12'})
        sinopse = sinopse[1].find('p').text
        if sinopse.startswith('Direção:'):
            sinopse = None
    except AttributeError:
        try:
            sinopse = sinopse[1].text.strip()
        except Exception:
            sinopse = None
    except IndexError:
        sinopse = None
    infos = tabelafilme.find_all('p', {'class': 'text-justify'})
    try:
        direcao = tabelafilme.find_all('a').text
    except AttributeError:
        try:
            direcao = tabelafilme.find('a').text
        except Exception:
            direcao = None

        ano = None
        duracao = None
        estado = None
        link_filme = None
        fonte = None
        obs = None

    for info in infos:
        if info.text.startswith('Ano de produção: '):
            ano = info.text.strip('Ano de produção: ').strip('"')
        elif info.text.startswith('Duração: '):
            duracao = info.text.strip('Duração: ').strip('"').strip("'")
        elif info.text.startswith('Estados produtores: '):
            estado = info.text.strip('Estados produtores:').strip('"').strip()
            if estado == 'Rio de Janei':
                estado = 'Rio de Janeiro'
            elif estado == 'São Paul':
                estado = 'São Paulo'
        elif info.text.startswith('Link do filme:'):
            link_filme = info.text.strip('Link do filme:').strip('"').strip()
        elif info.text.startswith('Fonte de pesquisa: '):
            fonte = info.text.strip('Fonte de pesquisa: ').strip('"')
        elif info.text.startswith('Observação:'):
            obs = info.text.strip('Observação:').strip()
    link_base = urlfilme
    codigo = idfilme
    try:
        cartaz = tabelafilme.find('div', {'class': 'col-lg-4'}).find('a')['href']
    except AttributeError:
        cartaz = None

    filme = Filme(titulo,
                 sinopse,
                 direcao,
                 ano,
                 duracao,
                 estado,
                 link_filme,
                 link_base,
                 codigo,
                 obs,
                 fonte,
                 cartaz)

    docbrasil.incluir_filme(filme)
    grava_filme(filme)

    print(f'{titulo}')


def grava_cabecalho():

    arquivo = open('docbrasil.csv', 'w', encoding='utf-8')
    gravacao = csv.writer(arquivo, lineterminator='\n')
    gravacao.writerow(['titulo',
                       'sinopse',
                       'direcao',
                       'ano',
                       'duracao',
                       'uf',
                       'link_filme',
                       'link_base',
                       'codigo',
                       'obs',
                       'fonte',
                       'cartaz',
                       'raspagem'])
    arquivo.close()


def grava_filme(filme):

    arquivo = open('docbrasil.csv', 'a', encoding='utf-8')
    gravacao = csv.writer(arquivo, lineterminator='\n')
    gravacao.writerow([filme.titulo,
                       filme.sinopse,
                       filme.direcao,
                       filme.ano,
                       filme.duracao,
                       filme.estado,
                       filme.link_filme,
                       filme.link_base,
                       filme.codigo,
                       filme.obs,
                       filme.fonte,
                       filme.cartaz,
                       time.strftime("%d/%m/%Y %H:%M:%S")])
    arquivo.close()


docbrasil = Colecao()
raspa_docbrasil()
