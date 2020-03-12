#!/usr/bin/env python3
#sudo cp ex1 /usr/local/bin

import fileinput
import re
import itertools

pares = []

def getTexto():
    texto = ""

    for line in fileinput.input():
        texto += line

    return texto

def entidades(texto):
    maius = r'(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.|[IVXLCDM]+)'
    de = r'(?:de|da|dos|das)' 
  
    s = r'\s+'
    ent = f"([^@\w])({maius}(?:{s}{maius}|{s}{de}{s}{maius})*)"

    texto = re.sub(ent, r'\1{\2}', texto)
    return texto

def frases(texto): ##Coloca @ no inicio das palavras que começam as frases
    exp1 = r'(\n\n+\s*)([A-Z])' ##refere-se as frases que iniciam os parágrafos
    exp2 = r'([a-z][.?!]+[\s]*)([A-Z])' ##refere-se as palavras após ponto final/exclamação/interrogação

    texto = re.sub(exp1,r'\1@\2',texto)
    texto = re.sub(exp2,r'\1@\2',texto)
    return texto


def getPairs(texto):
    frs = [] 
    frs = texto.split('@')
    for fr in frs:
        aux = re.findall('{[\w|\s]+}', fr) ##isto encontras as entidades da frase
        ents = []
        for e in aux:
            e = e[1:-1] ##retirar as chavetas, nao consegui apanhar sem elas
            ents.append(e)

        if len(ents) > 1:
            for pair in itertools.combinations(ents,2): ##gera combinaçoes e guarda os pares
                pares.append(pair)
            
        

##def cleanupPairs(texto):

getPairs(entidades(frases(getTexto())))