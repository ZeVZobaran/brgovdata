# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:34:37 2019
Funções utilitárias usadas como suporte para o pacote
@author: j_vz
"""
import requests
import json

def web_json_getter(link):
    '''
    Recebe um link que só tenha dados em JSON, baixa e retorna um dict
    '''
    res = requests.get(link)
    res.raise_for_status()
    json_dict = json.loads(res.text)
    return json_dict
