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

def frases(texto): ##Coloca @ no inicio das palavras que começam as frases
    exp1 = r'(\n\n+\s*)([A-Z])' ##refere-se as frases que iniciam os parágrafos
    exp2 = r'([a-z][.?!]+[\s]*)([A-Z])' ##refere-se as palavras após ponto final/exclamação/interrogação

    texto = re.sub(exp1,r'\1@\2',texto)
    texto = re.sub(exp2,r'\1@\2',texto)
    return texto


def entidades(texto):
    maius = r'(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.|[IVXLCDM]+)'
    de = r'(?:de|da|dos|das)' 
  
    s = r'\s+'
    ent = f"([^@\w])({maius}(?:{s}{maius}|{s}{de}{s}{maius})*)"

    texto = re.sub(ent, r'\1{\2}', texto)
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
    pairs = []
    ##Termos que aparecem a maiuscula mas que nao correspondem a entidades
    terms = ["I", "We", "Us", "They", "He", "Her", "Them", "It", "You", "Your", "My", "His", "And", "But", "Still", "Then", 
    "There", "That", "This", "The", "How","Now", "So", "Are", "Not", "Or", "What", "Where", "Which", "Why", "Well", "See", 
    "Something", "Thanks", "Stop", "Yes", "Yeah", "No", "In", "Oh", "Mrs", "Mr", "An", "All", "Just"]

    for p in pares:
        if p[0] not in terms and p[1] not in terms and p[0] != p[1]:
            pairs.append(p)
    
    return pairs


def groupAndRemove(pairs): ##Agrupa os pares com o respetivo nr de ocorrencias e remove os que têm menos que 5 ocorrencias
    pairOccur = {}
    for p in pairs:
        if p in pairOccur:
            occ = pairOccur.get(p)
            occ += 1
            pairOccur.update({p : occ})
        else:
            if (p[1],p[0]) in pairOccur:
                inv = (p[1],p[0])
                occ = pairOccur.get(inv)
                occ += 1
                pairOccur.update({inv : occ})
            else:
                pairOccur[p] = 1

    for k,v in list(pairOccur.items()): ##remover os que têm frequencia menor que 5
        if v < 5:
            pairOccur.pop(k)

    return pairOccur
    

def interpretador(pairOccur):
    char = input("Enter character from Harry Potter: ")
    top = input("Top K relationships: ")
    rels = {}
    i = 0
    for k,v in pairOccur.items():
        if k[0] == char or k[1] == char:
            rels[k] = v

    if len(rels) == 0:
        print("No relevant relationships found...")

    for w,v in sorted(rels.items(),key= lambda x : x[1], reverse=True):
        if i < int(top):
            print(w," --> ",v, "occurrences.")
            i+=1


p = getPairs(entidades(frases(getTexto())))
occur = groupAndRemove(cleanupPairs(p))
interpretador(occur)