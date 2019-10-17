# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 18:40:41 2019

Wrapper do API do SGS do BCB

@author: j_vz
"""

# %% Setup e lembretes
import pandas as pd
import datetime
from brgovdata.utils import web_json_getter


# %%

def _constr_base(serie):
    '''
    aux, recebe uma série e monta o inicio da URL invocadora
    '''
    return r'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados'.format(
            serie
            )


def sgs_por_data(serie, inicio, fim=False):
    '''
    Recebe uma serie, uma data inicial e uma final
    Retorna um dataframe com os valores, indexado pelas datas
    Se fim não for dado, usa a data de hoje
    Datas devem estar no format DD/MM/YYYY
    '''
    constr = _constr_base(serie)
    if not fim:
        fim = datetime.datetime.today().strftime('%d/%m/%Y')
    datas_constr = r'?formato=json&dataInicial={0}&dataFinal={1}'.format(
            inicio, fim
            )
    link = constr + datas_constr
    json_dict = web_json_getter(link)
    df = pd.DataFrame(json_dict)
    df.set_index('data', inplace=True)
    df.columns = [serie]
    return df


def sgs_por_n(serie, n):
    '''
    Recebe uma serie e uma quantidade n de periodos
    Retorna um dataframe com esses periodos, indexado pelas datas
    '''
    constr = _constr_base(serie)
    constr_n = r'/ultimos/{}?formato=json'.format(n)
    link = constr + constr_n
    json_dict = web_json_getter(link)
    df = pd.DataFrame(json_dict)
    df.set_index('data', inplace=True)
    df.columns = [serie]
    return df


def sgs_default(serie):
    '''
    Recebe uma série e retorna o DF padrão fornecido pelo BC
    '''
    link = _constr_base(serie)
    json_dict = web_json_getter(link)
    df = pd.DataFrame(json_dict)
    df.set_index('data', inplace=True)
    df.columns = [serie]
    return df


def sgs(series, n=False, inicio=False, fim=False):
    '''
    Recebe uma série uma uma lista de séries e retorna um dataframe com as
    series, indexado pelas datas
    '''
    if type(series) != list:
        series = [int(series)]  # Garante lista pra facilitar
    lista_df = []  # Lista auxiliar para montar os dataframes
    if n:
        for serie in series:
            df = sgs_por_n(serie, n)
            lista_df.append(df)
    elif inicio:
        for serie in series:
            df = sgs_por_data(serie, inicio, fim)
            lista_df.append(df)
    else:
        for serie in series:
            df = sgs_default(serie)
            lista_df.append(serie)
    result = pd.concat(lista_df, axis=1)
    return result


if __name__ == '__main__':
    serie = 20542
    series = [20542, 20543]
    n = 50
    inicio = '20/04/1998'
    fim = '20/04/2019'
    teste_1 = sgs_default(serie)
    teste_2 = sgs_por_n(serie, n)
    teste_3 = sgs_por_data(serie, inicio, fim)
    teste_4 = sgs_por_data(serie, inicio)
    teste_5 = sgs(series, n)
