# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:04:20 2019

downloaders de dados dos APIs do IBGE
Não inclui o API de notícias, acessivel em:
https://servicodados.ibge.gov.br/api/docs/noticias?versao=3
Não inclui o API de metadados, acessível em:
https://servicodados.ibge.gov.br/api/docs/metadados?versao=2
Não inclui os APIs de malha e localidade; pretendo adicionar
@author: j_vz
"""
# %% Setup e lembretes
import datetime
from brgovdata.utils import web_json_getter

# TODO adicionar malhas e localidades
# https://servicodados.ibge.gov.br/api/docs/localidades?versao=1
# https://servicodados.ibge.gov.br/api/docs/malhas?versao=2

# %% Funções


def info_agregados(
        agregado=False, metadados=False, periodos=-1, variaveis='all',
        localidade='BR', classificacao=False, **kwargs
        ):
    '''
    Acessa os dados do API que alimenta o SIDRA. Recomendo mais o uso de
    info_pesquisa, cujo formato é mais parecido com os dos dados divulgados
    pelo IBGE
    Se nenhum argumento é passado, retorna a lista de todos os agregados
    e seus IDs
    Agregado deve ser o número de um agregadod esejado (1705 para inflação, ex)
    Se metadados=True, retorna os metadados do agregado.
    Periodos refere-se aos pontos no tempo em que se quer o dado. 1 periodo
    normalmente é um mês, as vezes um trimestre. Pode ser:
            Uma data YYYYMM,
            Um intervalo de tempo {inicio}-{fim} no formato YYYYMM
            Um valor negativo (-6 para os ultimos 6 periodos do dado)
            Qualquer combinação dos acima, fornecidos em lista
        -1 por default
    variaveis pode ser 'allxp' para todas as variaveis, 'all' para todas e var
    percentuais, o codigo de uma variavel um uma lista de variaveis
    Localidade refere-se à região dos dados. Por default, Brasil. Para saber
    mais sobre os caveats da formatação de localidades do IBGE, veja a
    documentação do API em
    https://servicodados.ibge.gov.br/api/docs/agregados?versao=3
    Como é bem idiossincrático, não está generalizado. Se o parametro for dado,
    deve ser ser fornecido exatamente no formato pedido pelo IBGE
    O mesmo vale para classificacao, que permite restringir a busca ainda mais.
    Por exemplo, poderiamos acessar a produção agrária de abacaxi
    '''
    url = r'https://servicodados.ibge.gov.br/api/v3/agregados/'
    if not agregado:
        result = web_json_getter(url)
        return result
    link = url + agregado
    if metadados:
        link = link + '/metadados'
        result = web_json_getter(link)
        return result
    if type(periodos) == list:
        periodos = '|'.join(periodos)
    if type(variaveis) == list:
        variaveis = '|'.join(variaveis)
    link = link + '/periodos/{0}/variaveis/{1}'.format(periodos, variaveis)
    link = link + '?'
    if classificacao:
        link = link + 'classificacao={}&'.format(classificacao)
    link = link + 'localidade={}'.format(localidade)
    result = web_json_getter(link)
    return result


def info_calendario(pesquisa=False, de=False, ate=False, **kwargs):
    '''
    Retorna o calendário de divulgações (passado e futuro) da pesquisa
    Pesquisa pode ser o nome ou o ID da pesquisa
    Para mais informações, consultar info_produtos() ou o site do IBGE
    Se pesquisa não especificada, retorna o calendário completo do IBGE
    Se de e/ou até não são especificados, defaultam para hoje e daqui a um ano
    '''
    # TODO tratar a implementação de paging do IBGE
    if not de:
        de = datetime.datetime.today().strftime('%Y-%m-%d')
    if not ate:
        mais_ano = datetime.datetime.today() + datetime.timedelta(365)
        ate = mais_ano.strftime('%Y-%m-%d')
    link = r'https://servicodados.ibge.gov.br/api/v3/calendario/{0}/?{1}?{2}'\
        .format(pesquisa, de, ate)
    result = web_json_getter(link)
    return result


def info_publicaçoes(termo=False, **kwargs):
    '''
    Retorna as públicações que tem a ver com o termo de busca fornecido.
    '''
    # TODO tratar a implementação de paging do IBGE
    if not termo:
        raise TypeError('Forneça um termo de busca')
    link = r'http://servicodados.ibge.gov.br/api/v1/publicacoes/'
    link = link + termo
    result = web_json_getter(link)
    return result


def info_nomes(
        nomes=False, decada=False, sexo=False, estados=False, localidade=False,
        **kwargs
        ):
    '''
    Retorna a frequência do nome passado pela década de nascimento, ou o
        ranking de frequencias para cada década.
    Se nenhum argumento for fornecido, devolve o ranking geral para o brasil
    Por default, retorna a pesquisa unisex, para o Brasil inteiro.
    Sexo pode ser M ou F, estados pode ser True para agrupar os nomes por UF
    localidade pode ser o identificador de uma UF ou município (numérico)
    '''

    # Implementação de um XOR entre nomes e decadas
    assert ((nomes and not decada) or (not nomes and decada)),\
        'Forneça apenas um dentre nomes e decada'
    url = r'https://servicodados.ibge.gov.br/api/v2/censos/nomes/'
    if nomes:
        if type(nomes) == list:
            nomes = '|'.join(nomes)  # Concatena os nomes em string se lista
        link = url + nomes
    if decada:
        link = url + 'ranking'
        link = link + '?decada={}'.format(decada)
    if sexo:
        link = link + '?sexo={}'.format(sexo)
    if estados:
        link = link + '?groupBy={}'.format(estados)
    if localidade:
        link = link + '?localidade={}'.format(localidade)
    result = web_json_getter(link)
    return result


def info_populaçao(localidade='BR', **kwargs):
    '''
    Por enquanto, só possui a projeção de população do IBGE para hoje
    Conforme eles adicionem informações, será atualizado
    Pode receber um parametro de localidade para a projeção de população do
    lugar específico.
    Retorna a localidade, o horario da projeção e a projeção
    '''

    link = r'https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/'
    link = link + localidade
    result = web_json_getter(link)
    return result


def info_produtos(tipo=False, **kwargs):
    '''
    Retorna o ID, tipo, título (legível) e alias (identificador para maquinas)
    de cada produto do IBGE
    O tipo pode ser especificado
    '''
    url = r'https://servicodados.ibge.gov.br/api/v1/produtos/'
    tipos = ['estatistica', 'geociencias']
    tipo = tipo.lower()
    assert tipo in tipos, "Os produtos válidos são: {}. "\
        "Não especifique para receber todos".format(tipos)
    link = url + tipo
    result = web_json_getter(link)
    return result


def info_cnae(codigo=False, pedido=False, **kwargs):
    '''
    Manipula o API das classes CNAE.
    Recebe uma classe ou lista de classes da CNAE contendo até 5 algarismos
    Esquema da divisão da CNAE:
    1. Seção
       2. Divisão
         3. Grupo
           4. Classe
             5. Subclasse
               6. Atividade econômica
    Se apenas o código é explicitado, retorna as informações desse código
    Se apenas o pedido é especificado, retorna as informações do tipo.
    Se ambos, retorna as informações de {pedido} contidos em {código}.
    Atenção: Se o código for de uma subclasse, não se pode especificar pedido.
    O retorno já incluí as atividades econômicas
    '''

    tipos = ['secao', 'divisao', 'grupo', 'classe', 'subclasse']
    url = r'https://servicodados.ibge.gov.br/api/v2/cnae'
    assert (codigo or pedido), 'Especifique um código e/ou um tipo'

    if not codigo:
        # Se código não for passado, informa sobre o tipo pedido
        extensao = '/{}'.format(pedido)
        link = url + extensao
        result = web_json_getter(link)
        return result

    try:
        # Seleciona um codigo para examinar o que foi pedido
        exemplo = str(codigo[0])
        codigo = '|'.join(map(str, codigo))  # Se códigos em lista, concatena
    except TypeError:
        exemplo = str(codigo)
    # Identificando que tipo de código foi fornecido
    len_tipo = {
            1: tipos[0], 2: tipos[1], 3: tipos[2], 5: tipos[3], 7: tipos[4]
            }
    try:
        fornecido = len_tipo[len(exemplo)]
    except KeyError:
        raise IndexError('O código não deve conter mais de 7 algarismos')

    if not pedido or fornecido == tipos[4]:
        # Se o nível de onde a info deve vir não foi especificado
        # Ou se o nível for o menor possível
        extensao = '/{0}/{1}'.format(fornecido, codigo)
        link = url + extensao
        result = web_json_getter(link)
        return result

    pedido = pedido.lower()
    assert pedido in tipos, 'O tipo deve ser um de {}'.format(tipos)
    extensao = '/{0}/{1}/{2}'.format(fornecido, codigo, pedido)
    link = url + extensao
    result = web_json_getter(link)
    return result


def info_ibge(fonte, **kwargs):
    '''
    Wrapper pras funções info_
    Recebe a fonte e os argumentos
    Pega a função certa e passa os argumentos pra ela
    Retorna o retorno da função esoclhida
    Se nenhum match na fonte, erro
    '''
    fonte = fonte.lower()
    fontes_validas = [
            'cnae', 'calendario', 'agregados', 'produtos', 'publicaçoes',
            'nomes', 'populaçao'
            ]
    assert fonte in fontes_validas, 'Fontes válidas: {}'.format(fontes_validas)
    funcs = {
            fontes_validas[0]: info_cnae,
            fontes_validas[1]: info_calendario,
            fontes_validas[2]: info_agregados,
            fontes_validas[3]: info_produtos,
            fontes_validas[4]: info_publicaçoes,
            fontes_validas[5]: info_nomes,
            fontes_validas[6]: info_populaçao
            }
    func = funcs[fonte]
    result = func(**kwargs)
    return result


def sidra_getter(
        link_direto=False, tabela=False, periodos='last', variaveis='all',
        localidade='n1/1', classificacao=False, precisao='m'
        ):
    '''
    Invocador do WEBAPI do Sidra
    É possível fornecer o link da tabela já feito pelo parâmetro link_direto.
    Periodos são os periodos desejados, sempre em string:
        all,
        first n, para o primeiros n periods (mais antigos, n omissivei se =1)
        last n, idem
        YYYY, para um ano
        YYYY-YYYY, para o período entre o primeiro e o segundo ano,
        YYYY,YYYY para os dois anos em avulso,
        YYYYDD para o ponto (mes, trimestre, semestre, segundo o dado) no ano
        , e - para YYYYDD
        Quaisquer combinações das formas acima, separadas por vírgula
    O mesmo vale para variaveis, classificação e localidade.
    As especificações de localidade são idiossincráticas. Conferir no site.
    Precisão fornece a quantidade de casas decimais. Por default, o máximo.
    Para consultar os metadados de uma tabela específica,
    http://api.sidra.ibge.gov.br/
    Para documentação mais extensiva, http://api.sidra.ibge.gov.br/home/ajuda
    '''
    if link_direto:
        result = web_json_getter(link_direto)
        return result
    assert tabela, TypeError('Forneça um link_direto ou uma tabela')
    dados = '/t/{0}/p/{1}/v/{2}/{3}'.format(
            tabela, periodos, variaveis, localidade
            )
    if classificacao:
        dados = dados + '/' + classificacao
    formato = '/d' + str(precisao)
    link = r'http://api.sidra.ibge.gov.br/values{0}{1}'.format(dados, formato)
    result = web_json_getter(link)
    return result
