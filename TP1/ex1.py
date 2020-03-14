#!/usr/bin/env python3
#sudo cp ex1 /usr/local/bin

import fileinput
import re
import itertools


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
    pares = []
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
    return pares    
        

def cleanupPairs(pares):
    ##ssprint(len(pares))
    pairs = []
    ##Termos que aparecem a maiuscula mas que nao correspondem a entidades
    terms = ["I", "And", "They", "Well", "Now", "Then", "How", "My", "You", "Yes", "No", "In", "Oh", "An", "Yeh", "But",
     "He", "Still", "There", "See", "Mrs", "This", "It", "Stop", "Not", "Or", "Thanks", "What", "Where", "Something"]
    i = 0
    for p in pares:
        if p[0] not in terms and p[1] not in terms:
            pairs.append(p)
        else:
            i+=1
    
    ##print(i) ##Pares removidos
    ##print(len(pairs))
    return pairs


def freq(pairs):
    for p in pairs:
        i = pairs.count(p)
        if i<3:
          for j in range(0, i):
            pairs.remove(p)
    #print(pairs)
 

p = getPairs(entidades(frases(getTexto())))
freq(cleanupPairs(p))
print(cleanupPairs(p))